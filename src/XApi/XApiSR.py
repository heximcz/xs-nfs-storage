import operator
from dataclasses import dataclass
from src.XApi import XApiConnect

@dataclass(order=True)
class XApiOneStorage():
    """
    SR structure from XAPI

    uuid  :  7590b1d2-521a-2ccb-92e8-f1192b18a76c
    name_label  :  STORAGE 01
    name_description  :  NFS SR [172.44.1.5:/xcpng/xenserver]
    allowed_operations  :  ['vdi_enable_cbt', 'vdi_list_changed_blocks', 'unplug', 'plug', 'pbd_create', 'vdi_disable_cbt', 'update', 'pbd_destroy', 'vdi_resize', 'vdi_clone', 'vdi_data_destroy', 'scan', 'vdi_snapshot', 'vdi_mirror', 'vdi_create', 'vdi_destroy', 'vdi_set_on_boot']
    current_operations  :  {}
    VDIs  :  ['OpaqueRef:e8488b6a-c065-4268-9ddc-ece2b6f87340', 'OpaqueRef:614c4a02-1a99-4069-9ccd-8c1e30e4cc63', 'OpaqueRef:b775029f-f612-4329-8c9e-fc7b19ef5af1', 'OpaqueRef:7163fd51-8388-44c5-a528-3fccf33bf01d']
    PBDs  :  ['OpaqueRef:0da73f11-61e7-48cf-aa1d-0a533baa9955']
    virtual_allocation  :  85899345920
    physical_utilisation  :  8774483968
    physical_size  :  309178925056
    type  :  nfs
    content_type  :  user
    shared  :  True
    other_config  :  {'auto-scan': 'true'}
    tags  :  []
    sm_config  :  {}
    blobs  :  {}
    local_cache_enabled  :  False
    introduced_by  :  OpaqueRef:NULL
    clustered  :  False
    is_tools_sr  :  False
    """

    sr_uuid: str
    sr_name_label: str
    sr_name_description: str
    sr_vdis: list

    # print class as str
    def __str__(self):
        return f"SR uuid: {self.sr_uuid}, SR name_label: {self.sr_name_label}, SR name_description: {self.sr_name_description}"

    def __repr__(self):
        return str(self)

class XApiStorageRepositories:
    """
    Find NFS SR from XAPI
    """

    def __init__(self, xapi: XApiConnect) -> None:
        self.__xapi = xapi
        self.__all_sr: list[XApiOneStorage] = []

    def set_SRs(self) -> None:
        """
        Set list[XApiOneStorage]
        """
        self.__create_sr_list()

    def get_SRs(self) -> list[XApiOneStorage]:
        """
        :return: sorted(list[XApiOneStorage])
        """
        return sorted(self.__all_sr, key=operator.attrgetter("sr_name_label"))

    def __create_sr_list(self) -> None:
        """
        Get data from NFS SRs and create list of dataclasses
        :return: None
        """
        all_sr = self.__xapi.session.xenapi.SR.get_all()
        for sr in all_sr:
            record = self.__xapi.session.xenapi.SR.get_record(sr)
            if (record["type"] == "nfs"):
                self.__all_sr.append(
                    XApiOneStorage(
                        sr_uuid = record["uuid"],
                        sr_name_label = record["name_label"],
                        sr_name_description = record["name_description"],
                        sr_vdis = record["VDIs"]
                        )
                    )
