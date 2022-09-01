import os, sys
import XenAPI
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
        Add actual running version of vdi (SR and VM) to database
        """
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


        ### all to db ###

        # Create new version id
        db = XApiMysql(self.__config)
        version_id = db.create_new_version()

        # all virtual machines
        vms = vm.get_VMs()
        for one_vm in vms:
            # VM uuid: 0e16dc5f-a169-c322-2790-fa4e3ca3e47f | 
            # VM name_label: Deb11 shapshot on SR01 | 
            # VM is_a_snapshot: True | 
            # 
            # VBD(object):
            # VBD uuid: 2b24c5d5-e0d4-52ed-1c3e-6bf367b1381a | 
            # VBD device: xvda | 
            # 
            # VDI(object): 
            # VDI uuid: 71e5b355-e09d-435c-ade0-f052ddf7df5f | 
            # VDI is_a_snapshot: True | 
            # VDI name_label: Debian 11x2 on ZFS SR01 0 | 
            # 
            # SR(object): 
            # SR uuid: 7590b1d2-521a-2ccb-92e8-f1192b18a76c, 
            # SR name_label: STORAGE 01, 
            # SR name_description: NFS SR [172.44.1.5:/xcpng/xenserver]

            # 1. add SR
            # 2. add VM
            # 3. add VDI
            sr_id = db.add_sr(one_vm.vbd.vdi.sr, version_id)
            vm_id = db.add_vm(one_vm, version_id)
            db.add_vdi(one_vm.vbd.vdi, version_id, sr_id, vm_id, one_vm.vbd.vbd_device)
