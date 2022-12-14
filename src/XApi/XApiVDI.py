from dataclasses import dataclass
from src.XApi.XApiConnect import XApiConnect
from src.XApi.XApiSR import XApiOneStorage

@dataclass
class XApiOneVdi():
    """
    VDI structure from XAPI

    uuid  :  71e5b355-e09d-435c-ade0-f052ddf7df5f
    name_label  :  Debian 11x2 on ZFS SR01 0
    name_description  :  Created by template provisioner
    allowed_operations  :  ['generate_config', 'update', 'forget',
        'destroy', 'snapshot', 'resize', 'copy', 'clone']
    current_operations  :  {}
    SR  :  OpaqueRef:984e8e56-b685-4a19-9640-aeddfa2e5652
    VBDs  :  ['OpaqueRef:5c1c82ca-8e67-461b-904b-688c736ed58d']
    crash_dumps  :  []
    virtual_size  :  21474836480
    physical_utilisation  :  46592
    type  :  system
    sharable  :  False
    read_only  :  False
    other_config  :  {'content_id': '28be196d-81e0-165c-93ef-e51157c92d9a'}
    storage_lock  :  False
    location  :  71e5b355-e09d-435c-ade0-f052ddf7df5f
    managed  :  True
    missing  :  False
    parent  :  OpaqueRef:NULL
    xenstore_data  :  {}
    sm_config  :  {'vhd-parent': '3a62fc55-3544-405d-bab8-84fd566bee7a'}
    is_a_snapshot  :  True
    snapshot_of  :  OpaqueRef:b775029f-f612-4329-8c9e-fc7b19ef5af1
    snapshots  :  []
    snapshot_time  :  20220830T13:59:24Z
    tags  :  []
    allow_caching  :  False
    on_boot  :  persist
    metadata_of_pool  :  OpaqueRef:NULL
    metadata_latest  :  False
    is_tools_iso  :  False
    cbt_enabled  :  False
    """

    vdi_uuid: str
    vdi_name_label: str
    vdi_vbds: list
    vdi_is_a_snapshot: bool
    sr: XApiOneStorage

    def __str__(self):
        return f"VDI uuid: {self.vdi_uuid} | VDI is_a_snapshot: {self.vdi_is_a_snapshot} | VDI name_label: {self.vdi_name_label} | SR(object): {self.sr}"

    def __repr__(self):
        return str(self)

class XApiVdiList:
    """
    Find VDIs data from XAPI
    """

    def __init__(self, xapi: XApiConnect) -> None:
        self.__xapi = xapi
        self.__all_vdi: list[XApiOneVdi] = []

    def set_VDIs(self, nfs_srs: list[XApiOneStorage]) -> None:
        """
        Set list[XApiOneVdi]
        """
        for one_sr in nfs_srs:
            self.__create_vdi_list(one_sr)

    def get_VDIs(self) -> list[XApiOneVdi]:
        """
        :return: list[XApiOneVdi]
        """
        return self.__all_vdi

    def __create_vdi_list(self, one_sr: XApiOneStorage) -> None:
        """
        Get data from VDI and append new XApiOneVdi dataclasses to "all_vdi" list
        :return: None
        """

        # nacti jednotlive VDI do dataclass listu
        for one_vdi_or in one_sr.sr_vdis:
            record = self.__xapi.session.xenapi.VDI.get_record(one_vdi_or)
            self.__all_vdi.append(
                XApiOneVdi(
                    vdi_uuid = record["uuid"],
                    vdi_name_label = record["name_label"],
                    vdi_vbds = record["VBDs"],
                    vdi_is_a_snapshot = record["is_a_snapshot"],
                    sr = one_sr
                    )
                )
