from src.MySQL import MySQL
from src.Config import LoadConfig
from src.XApi.XApiSR import XApiOneStorage
from src.XApi.XApiVM import XApiOneVm
from src.XApi.XApiVDI import XApiOneVdi

class XApiMysql(MySQL):

    def __init__(self, config: LoadConfig) -> None:
        super().__init__(config)

    def create_new_version(self) -> int:
        """
        Create new version ID
        :return: int
        """

        return self._insert("""
            INSERT INTO `version` (`created`) VALUES (current_timestamp());
            """)

    def add_sr(self, one_sr: XApiOneStorage, version_id: int) -> int:
        """
        Add new SR to db or search exist SR and return SR id in db
        :return: int
        """

        # find SR
        id = self._fetch_one(f"""
            SELECT id FROM `storages` WHERE `version` = '{version_id}' AND `uuid` = '{one_sr.sr_uuid}'
            """)
        if id:
            return int(id[0])

        # SR uuid not in db, create new row
        return self._insert(f"""
            INSERT INTO `storages` 
            (`version`, `uuid`, `name_label`, `name_description`) 
            VALUES
            ('{version_id}', '{one_sr.sr_uuid}', '{one_sr.sr_name_label}', '{one_sr.sr_name_description}');
            """)

    def add_vm(self, one_vm: XApiOneVm, version_id: int) -> int:
        """
        Add new VM to db or search exist VM and return VM id in db
        :return: int
        """
        
        # find VM
        id = self._fetch_one(f"""
            SELECT id FROM `vm` WHERE `version` = '{version_id}' AND `uuid` = '{one_vm.vm_uuid}'
            """)
        if id:
            return int(id[0])

        # VM uuid not in db, create new row
        return self._insert(f"""
            INSERT INTO `vm` (`version`, `uuid`, `name_label`, `name_description`, `snapshot`)
            VALUES ('{version_id}', '{one_vm.vm_uuid}', '{one_vm.vm_name_label}', '{one_vm.vm_name_description}', '{one_vm.vm_is_a_snapshot}');
            """)

    def add_vdi(self, one_vdi: XApiOneVdi, version_id: int, sr_id: int, vm_id: int, vbd_device: str) -> None:
        """
        Add new VDI for VM to db
        :return: None
        """
        
        # VM uuid not in db, create new row
        self._insert(f"""
            INSERT INTO `vdi` (`version`, `vm`, `storage`, `uuid`, `name_label`, `snapshot`, `vbd_device`)
            VALUES
            ('{version_id}', '{vm_id}', '{sr_id}', '{one_vdi.vdi_uuid}',
             '{one_vdi.vdi_name_label}', '{one_vdi.vdi_is_a_snapshot}', '{vbd_device}')
            """)

    def _insert(self, command: str) -> int:
        """
        Insert new row. Return row id.
        :return: int
        """
        my_cursor = self._mydb.cursor()
        my_cursor.execute(command)
        self._mydb.commit()
        my_cursor.close()
        return my_cursor.lastrowid

    def _fetch_one(self, command: str) -> int:
        """
        Fetch one row. Return row id.
        :return: int
        """
        my_cursor = self._mydb.cursor()
        my_cursor.execute(command)
        id = my_cursor.fetchone()
        my_cursor.close()
        return id
