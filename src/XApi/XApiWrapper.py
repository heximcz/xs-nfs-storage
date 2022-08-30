from src.Config import LoadConfig
from src.XApi.XApiConnect import XApiConnect
from src.XApi.XApiSR import XApiStorageRepositories, XApiOneStorage
from src.XApi.XApiVDI import XApiVdiList, XApiOneVdi
from src.MySQL import MySQL

class XApiWrapper:
    """
    funkce
    """
    
    def __init__(self, config: LoadConfig) -> None:
        self.__config = config
        self.__mysql = MySQL(config)
        self.__xapi = XApiConnect(config)
    
    def update_sr(self):
        """
        Add new NFS SR and update changes in name-label and name-description.
        :return: None
        """

        # load NFS SRs from xapi
        sr = XApiStorageRepositories(self.__xapi)
        xapi_all_nfs_sr: list[XApiOneStorage] = sr.get_Storages()
        # compare xapi and mysql SRs by uuid, add new or update changes
        for xapi_sr in xapi_all_nfs_sr:
            sr_data = self.__mysql.get_sr_by_uuid(xapi_sr.sr_uuid)
            if sr_data is None:
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
        All in One

        sr-list - obsahuje nazvy a uuid NFS SR
        vm-list - obsahuje nazvy VM
        sr-file-name - obsahuje nazev souboru (disků) danneho VM a nazev disku v xenu

        Novy postup:
        1. zacit nactenim SR, jejich zaznam ma vsechny vdi na tom SR
        2. ze SR nacist jen VDI SR
        3. poracovat stejne dal jako v testu

        """
        # load NFS SRs from xapi
        sr = XApiStorageRepositories(self.__xapi)
        nfs_srs: list[XApiOneStorage] = sr.get_Storages()

        # one SR, many VDIs
        all_vdi: list[XApiOneVdi] = []
        vdi = XApiVdiList(self.__config, self.__xapi)
        for one_sr in nfs_srs:
            vdi.append_VDIs(one_sr, all_vdi)

        print(all_vdi)
        # mam vsechny VDIcka ze vsech SR
        #  
