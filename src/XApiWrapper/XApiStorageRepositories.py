from dataclasses import dataclass
from src.XApiWrapper import XApiConnect


class XApiStorageRepositories:

    def __init__(self, xapi: XApiConnect) -> None:
        self.xapi = xapi
        self.__one_sr: list[XApiOneStorage] = []

    def get_Storages(self) -> list:
        all_sr = self.xapi.session.xenapi.SR.get_all()
        for sr in all_sr:
            record = self.xapi.session.xenapi.SR.get_record(sr)
            if (record["type"] == "nfs"):
                self.__one_sr.append(XApiOneStorage(record["uuid"], record["name_label"], record["name_description"]))
        return self.__one_sr

@dataclass
class XApiOneStorage():

    def __init__(self,sr_uuid: str, sr_name_label: str, sr_name_description: str) -> None:
        self.__sr_uuid: str = sr_uuid
        self.__sr_name_label: str = sr_name_label
        self.__sr_name_description: str = sr_name_description
    
    def get_sr_uuid(self) -> str:
        return self.__sr_uuid
    
    def get_sr_name_label(self) -> str:
        return self.__sr_name_label

    def get_sr_name_description(self) -> str:
        return self.__sr_name_description

    # print class as str
    def __str__(self):
        return "Storage uuid: %s, Name Label: %s, Name Description: %s" % (self.__sr_uuid, self.__sr_name_label, self.__sr_name_description)

    def __repr__(self):
        return str(self)