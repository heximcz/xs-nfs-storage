import os, sys
import XenAPI
from src.Config import LoadConfig
from src.XApi.XApiConnect import XApiConnect
from src.XApi.XApiSR import XApiStorageRepositories
from src.XApi.XApiVDI import XApiVdiList
from src.XApi.XApiVBD import XApiVbdList
from src.XApi.XApiVM import XApiVmList
from src.MySQL import MySQL

class XApiWrapper:
    """
    Check all disk od all NFS SRs
    Put actual version to database

    Just run()
    """
    
    def __init__(self, config: LoadConfig) -> None:
        self.__config = config
        self.__mysql = MySQL(config)
        self.__xapi = XApiConnect(config)
    
    # def update_sr(self):
    #     """
    #     Add new NFS SR and update changes in name-label and name-description.
    #     :return: None
    #     """

    #     # load NFS SRs from xapi
    #     sr = XApiStorageRepositories(self.__config, self.__xapi)
    #     xapi_all_nfs_sr: list[XApiOneStorage] = sr.get_Storages()
    #     # compare xapi and mysql SRs by uuid, add new or update changes
    #     for xapi_sr in xapi_all_nfs_sr:
    #         sr_data = self.__mysql.get_sr_by_uuid(xapi_sr.sr_uuid)
    #         if sr_data is None:
    #             # pridej nove SR do DB
    #             self.__mysql.add_new_sr(
    #                 xapi_sr.sr_uuid,
    #                 xapi_sr.sr_name_label,
    #                 xapi_sr.sr_name_description
    #                 )
    #         else:
    #             # aktualizuj hodnoty (muze se zmenit name label nebo description) v pripade zmeny
    #             if xapi_sr.sr_name_label != sr_data[2] or xapi_sr.sr_name_description != sr_data[3]:
    #                 self.__mysql.update_sr(
    #                     xapi_sr.sr_uuid, 
    #                     xapi_sr.sr_name_label, 
    #                     xapi_sr.sr_name_description
    #                     )
    #     self.__config.logger.info("SR_List - Updated.")

    def run(self):
        """
        All in One

        sr-list - obsahuje nazvy a uuid NFS SR
        vm-list - obsahuje nazvy VM
        sr-file-name - obsahuje nazev souboru (disků) danneho VM a nazev disku v xenu

        Novy postup:
        1. zacit nactenim SR, jejich zaznam ma vsechny vdi na tom SR
        2. ze SR nacist jen VDI SR
        3. proskenuj VBDs v VDIs a prirad spravne VM
        4. nasypat to do databaze

        """
        try:
            self.__xapi.open()

            # NFS SRs from xapi
            sr = XApiStorageRepositories(self.__xapi)

            # set VDIs from SR
            vdi = XApiVdiList(self.__xapi)
            vdi.set_VDIs(sr.get_NFS_Storages())

            # set VBDs from VDIs
            vbd = XApiVbdList(self.__xapi)
            vbd.set_VBDs(vdi.get_VDIs())

            # finally set VM from VBDs
            vm = XApiVmList(self.__xapi)
            vm.set_VMs(vbd.get_VBDs())

        except XenAPI.XenAPI.Failure as e:
            self.__config.logger.error(e)
            sys.exit(os.EX_UNAVAILABLE)
        finally:
            self.__xapi.close()

        print(vm.get_VMs())

        # TODO nasypat data do databaze
        # ? jak zjistit pripadne zmeny v uuid
        # ? resit to, nebo ne
        # ? verzovani v databazi a ukladat vzdy novou
        # ? nebo jit stylem: prvni inicializace a pak jen aktualizace podle dat v databazi.
        # verzovani by bylo lepsi, pak staci udelat rutina ma mazani starych verzi

