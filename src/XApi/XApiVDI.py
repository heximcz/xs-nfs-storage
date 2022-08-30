from dataclasses import dataclass
from src.XApi import XApiConnect


class XApiVdiList:

    def __init__(self, xapi: XApiConnect) -> None:
        self.__xapi = xapi

    def get_VDIs(self) -> list:
        vdi: list[XApiOneVdi] = []
        
        # zjisti vsechny idenfifikatory VDI. Vraci list OpaqueRef VDIs
        all_vdi_or = self.__xapi.session.xenapi.VDI.get_all()
        
        for one_vdi_or in all_vdi_or:
            record = self.__xapi.session.xenapi.VDI.get_record(one_vdi_or)
            vdi.append(
                XApiOneVdi(
                    vdi_uuid = record["uuid"],
                    vdi_name_label = record["name_label"],
                    vdi_sr = record["SR"],
                    vdi_vbds = record["VBDs"],
                    vdi_is_a_snapshot = record["is_a_snapshot"]
                    )
                )
        return vdi

@dataclass
class XApiOneVdi():
    """
    VDI RECORD:
    uuid  :  71e5b355-e09d-435c-ade0-f052ddf7df5f
    name_label  :  Debian 11x2 on ZFS SR01 0
    name_description  :  Created by template provisioner
    allowed_operations  :  ['generate_config', 'update', 'forget', 'destroy', 'snapshot', 'resize', 'copy', 'clone']
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
    vdi_sr: str
    vdi_vbds: list
    vdi_is_a_snapshot: bool
    
    # print class as str
    def __str__(self):
        return "VDI uuid: %s | Is Snapshot: %s | Name Label: %s" % (self.vdi_uuid, self.vdi_is_a_snapshot, self.vdi_name_label)

    def __repr__(self):
        return str(self)