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
                self.__one_sr.append(
                    XApiOneStorage(
                        sr_uuid = record["uuid"],
                        sr_name_label = record["name_label"],
                        sr_name_description = record["name_description"]
                        )
                    )
        return self.__one_sr

@dataclass
class XApiOneStorage():

    sr_uuid: str
    sr_name_label: str
    sr_name_description: str
    
    # print class as str
    def __str__(self):
        return "Storage uuid: %s, Name Label: %s, Name Description: %s" % (self.sr_uuid, self.sr_name_label, self.sr_name_description)

    def __repr__(self):
        return str(self)