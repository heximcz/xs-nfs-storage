import os, sys
import XenAPI
import mysql.connector
from src.Config import LoadConfig
from src.XApi.XApiConnect import XApiConnect
from src.XApi.XApiSR import XApiStorageRepositories
from src.XApi.XApiVDI import XApiVdiList
from src.XApi.XApiVBD import XApiVbdList
from src.XApi.XApiVM import XApiVmList
from src.XApi.XApiDatabase import XApiMysql

class XApiWrapper:
    """
    Check all disk od all NFS SRs
    Put actual version to database

    Just run()
    """
    
    def __init__(self, config: LoadConfig) -> None:
        self.__config = config
        self.__xapi = XApiConnect(config)
    
    def run(self):
        """
        Add actual running version of VDIs (SRs and VMs) to database
        """

        # generate lists from xapi
        try:
            self.__xapi.open()

            # NFS SRs from xapi
            sr = XApiStorageRepositories(self.__xapi)
            sr.set_SRs()

            # set VDIs from SR
            vdi = XApiVdiList(self.__xapi)
            vdi.set_VDIs(sr.get_SRs())

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

        # save new generated version to db
        try:

            db = XApiMysql(self.__config)

            # create new version ID
            version_id = db.create_new_version()

            # get all virtual machines list
            vms = vm.get_VMs()
            for one_vm in vms:
                # add SR to db
                sr_id = db.add_sr(one_vm.vbd.vdi.sr, version_id)
                # add VM to db
                vm_id = db.add_vm(one_vm, version_id)
                if vm_id is None:
                    raise mysql.connector.errors.ProgrammingError("HERE IS NO VM ID!")
                # add VDI to db
                db.add_vdi(one_vm.vbd.vdi, version_id, sr_id, vm_id, one_vm.vbd.vbd_device)

        except mysql.connector.errors.ProgrammingError as err:
            self.__config.logger.error(f"Error Code: {err.errno} | SQLSTATE: {err.sqlstate} | Message: {err.msg}")
            sys.exit(os.EX_UNAVAILABLE)

        # TODO add delete method - delete x-days older
        # TODO add print reconstruction output from db
