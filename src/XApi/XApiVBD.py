from dataclasses import dataclass
from src.XApi.XApiConnect import XApiConnect
from src.XApi.XApiVDI import XApiOneVdi

@dataclass
class XApiOneVbd():
    """
    VBD structure from XAPI

    uuid  :  2b24c5d5-e0d4-52ed-1c3e-6bf367b1381a
    allowed_operations  :  []
    current_operations  :  {}
    VM  :  OpaqueRef:7ec3fbea-0daa-4680-aec4-e1990622905b
    VDI  :  OpaqueRef:e8488b6a-c065-4268-9ddc-ece2b6f87340
    device  :  xvda
    userdevice  :  0
    bootable  :  False
    mode  :  RW
    type  :  Disk
    unpluggable  :  True
    storage_lock  :  False
    empty  :  False
    other_config  :  {'owner': 'true'}
    currently_attached  :  False
    status_code  :  0
    status_detail  :  
    runtime_properties  :  {}
    qos_algorithm_type  :  
    qos_algorithm_params  :  {}
    qos_supported_algorithms  :  []
    metrics  :  OpaqueRef:f3efd52a-2079-45d8-b49e-1c19e58325f8
    """

    vbd_uuid: str
    vbd_vm: str
    vbd_vdi: str
    vbd_device: str
    vdi: XApiOneVdi

    def __str__(self):
        return f"VBD uuid: {self.vbd_uuid} | VDI(object): {self.vdi}"

    def __repr__(self):
        return str(self)

class XApiVbdList:
    """
    VBDs
    """

    def __init__(self, xapi: XApiConnect) -> None:
        self.__xapi = xapi
        self.__all_vbd: list[XApiOneVbd] = []

    def set_VBDs(self, vdis: list[XApiOneVdi]) -> None:
        """
        Set list[XApiOneVbd]
        """
        self.__xapi.open()
        for one_vdi in vdis:
            self.__create_vbd_list(one_vdi)

    def get_VBDs(self) -> list[XApiOneVbd]:
        """
        Return list[XApiOneVbd]
        """
        return self.__all_vbd

    def __create_vbd_list(self, one_vdi: XApiOneVdi) -> None:
        """
        Get data from VBD and append new XApiOneVbd dataclasses to "all_vbd" list
        :return: None
        """

        # nacti jednotlive VBD do dataclass listu
        for one_vbd_or in one_vdi.vdi_vbds:
            record = self.__xapi.session.xenapi.VBD.get_record(one_vbd_or)
            self.__all_vbd.append(
                XApiOneVbd(
                    vbd_uuid = record["uuid"],
                    vbd_vm = record["VM"],
                    vbd_vdi = record["VDI"],
                    vbd_device = record["device"],
                    vdi = one_vdi
                    )
                )
