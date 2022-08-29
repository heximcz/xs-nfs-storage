from distutils.command.config import config
from src.Config import LoadConfig
from src.XApiWrapper import XApiConnect, XApiStorageRepositories, XApiOneStorage
from src.MySQL import MySQL

class XApiWrapper:
    """
    Cely system je postaven na OpaqueRef. OpaqueRef je jednoznacny identifikator v databazi xenu, uuid je totiz jen takony nejaky nazev.
    """
    
    def __init__(self, config: LoadConfig) -> None:
        self.__config = config
        self.__mysql = MySQL(config)
        self.__xapi = XApiConnect(config)
    
    def __close_session(self):
        """
        Close session
        :return: None
        """
        if self.__xapi.session:
            self.__xapi.close()

    def update_sr(self):
        """
        Add new NFS SR and update changes in name-label and name-description.
        :return: None
        """

        # load NFS SRs from xapi
        sr = XApiStorageRepositories(self.__xapi)
        xapi_all_nfs_sr: list[XApiOneStorage] = sr.get_Storages()
        self.__close_session()
        # compare xapi and mysql SRs by uuid, add new or update changes
        for xapi_sr in xapi_all_nfs_sr:
            sr_data = self.__mysql.get_sr_by_uuid(xapi_sr.sr_uuid)
            if  sr_data is None:
                # pridej nove SR do DB
                self.__mysql.add_new_sr(
                    xapi_sr.sr_uuid,
                    xapi_sr.sr_name_label,
                    xapi_sr.sr_name_description
                    )
            else:
                # aktualizuj hodnoty (muze se zmenit name label nebo description) v pripade zmeny
                if xapi_sr.sr_name_label != sr_data[2] or xapi_sr.sr_name_description != sr_data[3]:
                    self.__mysql.update_sr(
                        xapi_sr.sr_uuid, 
                        xapi_sr.sr_name_label, 
                        xapi_sr.sr_name_description
                        )
        self.__config.logger.info("SR_List - Updated.")

    def update_vdi(self):
        """
        mysql tabulky

sr-list - obsahuje nazvy a uuid NFS SR
vm-list - obsahuje nazvy VM
sr-file-name - obsahuje nazev souboru (disků) danneho VM a nazev disku v xenu

# xe vdi-list sr-uuid=7590b1d2-521a-2ccb-92e8-f1192b18a76c params=all managed=true 

uuid vdi:                 uuid ( RO) : 6bbd6c4d-226d-46d3-8280-7cfd34acbad2
nazev disku:              name-label ( RW): Debian 11x2 on ZFS SR01 0
        name-description ( RW): Created by template provisioner
           is-a-snapshot ( RO): false
             snapshot-of ( RO): <not in database>
               snapshots ( RO): 
           snapshot-time ( RO): 19700101T00:00:00Z
      allowed-operations (SRO): generate_config; update; forget; destroy; snapshot; resize; copy; clone
      current-operations (SRO): 
                 sr-uuid ( RO): 7590b1d2-521a-2ccb-92e8-f1192b18a76c
           sr-name-label ( RO): STORAGE 01
               vbd-uuids (SRO): e4827cf2-bb9e-ba15-7e6a-5eb591c3099e
         crashdump-uuids (SRO): 
            virtual-size ( RO): 21474836480
    physical-utilisation ( RO): 3422974464
                location ( RO): 6bbd6c4d-226d-46d3-8280-7cfd34acbad2
                    type ( RO): System
                sharable ( RO): false
               read-only ( RO): false
            storage-lock ( RO): false
                 managed ( RO): true
     parent ( RO) [DEPRECATED]: <not in database>
                 missing ( RO): false
            is-tools-iso ( RO): false
            other-config (MRW): content_id: 28be196d-81e0-165c-93ef-e51157c92d9a
           xenstore-data (MRO): 
               sm-config (MRO): 
                 on-boot ( RW): persist
           allow-caching ( RW): false
         metadata-latest ( RO): false
        metadata-of-pool ( RO): <not in database>
                    tags (SRW): 
             cbt-enabled ( RO): false

# xe vbd-list vdi-uuid=6bbd6c4d-226d-46d3-8280-7cfd34acbad2 params=all

uuid ( RO)                        : e4827cf2-bb9e-ba15-7e6a-5eb591c3099e
                     vm-uuid ( RO): fb37964e-a7e7-a5bf-c1b5-02ae064223da
               vm-name-label ( RO): Debian 11 on SR01
                    vdi-uuid ( RO): 6bbd6c4d-226d-46d3-8280-7cfd34acbad2
              vdi-name-label ( RO): Debian 11x2 on ZFS SR01 0
          allowed-operations (SRO): attach
          current-operations (SRO): 
                       empty ( RO): false
                      device ( RO): xvda
                  userdevice ( RW): 0
                    bootable ( RW): false
                        mode ( RW): RW
                        type ( RW): Disk
                 unpluggable ( RW): true
          currently-attached ( RO): true
                  attachable ( RO): <expensive field>
                storage-lock ( RO): false
                 status-code ( RO): 0
               status-detail ( RO): 
          qos_algorithm_type ( RW): 
        qos_algorithm_params (MRW): 
    qos_supported_algorithms (SRO): 
                other-config (MRW): owner: true
                 io_read_kbs ( RO): <expensive field>
                io_write_kbs ( RO): <expensive field>

# ls -lsa /xcpng/xenserver/7590b1d2-521a-2ccb-92e8-f1192b18a76c/

7437928 -rw-r--r-- 1 nobody nogroup 17217667584 Aug 28 21:37 5edcc1ca-4d46-443a-8611-d7b748944fbf.vhd
1129837 -rw-r--r-- 1 nobody nogroup  3422974464 Aug 28 22:41 6bbd6c4d-226d-46d3-8280-7cfd34acbad2.vhd

        """
