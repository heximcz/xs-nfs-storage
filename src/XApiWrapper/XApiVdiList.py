from dataclasses import dataclass
from src.XApiWrapper import XApiConnect


class XApiVdiList:

    def __init__(self, xapi: XApiConnect) -> None:
        self.xapi = xapi

    def get_Storages(self) -> list:
        pass


@dataclass
class XApiOneVdi():

    # sr_uuid: str
    # sr_name_label: str
    # sr_name_description: str
    
    # print class as str
    def __str__(self):
        return "Storage uuid: %s, Name Label: %s, Name Description: %s" % (self.sr_uuid, self.sr_name_label, self.sr_name_description)

    def __repr__(self):
        return str(self)