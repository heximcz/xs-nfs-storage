from distutils.command.config import config
from src.Config import LoadConfig
from src.XApiWrapper import XApiConnect, XApiStorageRepositories, XApiOneStorage
from src.MySQL import MySQL

class XApiWrapper:
    
    def __init__(self, config: LoadConfig) -> None:
        self.__config = config
        self.__xapi = XApiConnect(config)
        self.__mysql = MySQL(config)
    
    def run(self):

        # load NFS SRs from xapi
        sr = XApiStorageRepositories(self.__xapi)
        xapi_all_nfs_sr = sr.get_Storages()
        self.__xapi.close()
        # compare xapi and mysql SRs by uuid, add new or update changes
        self.__check_sr(xapi_all_nfs_sr)

    def __check_sr(self, xapi_all_nfs_sr: XApiOneStorage) -> None:
        # print("Pridat nove SR do db:")
        for xapi_sr in xapi_all_nfs_sr:
            sr_data = self.__mysql.get_sr_by_uuid(xapi_sr.get_sr_uuid())
            if  sr_data is None:
                # pridej nove SR do DB
                self.__mysql.add_new_sr(xapi_sr.get_sr_uuid(), xapi_sr.get_sr_name_label(), xapi_sr.get_sr_name_description())
            else:
                # aktualizuj hodnoty (muze se zmenit name label nebo description) v pripade zmeny
                if xapi_sr.get_sr_name_label() != sr_data[2] or xapi_sr.get_sr_name_description() != sr_data[3]:
                    self.__mysql.update_sr(xapi_sr.get_sr_uuid(), xapi_sr.get_sr_name_label(), xapi_sr.get_sr_name_description())
