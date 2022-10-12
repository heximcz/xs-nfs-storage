from src.Config import LoadConfig
from src.MySQL.MySQL import MySQL

class VDIMySQL(MySQL):

    def __init__(self, config: LoadConfig) -> None:
        super().__init__(config)

    def get_versions(self) -> list:
        """
        Get all saved versions
        """
        versions = self._fetch_all(f"""
            SELECT * FROM `version` ORDER BY id DESC
            """)
        return versions

    def get_vms(self, version: int) -> list:
        """
        Get all vm from specific saved version
        """
        versions = self._fetch_all(f"""
            SELECT 
            vm.uuid as vm_uuid,
            vm.name_label as vm_name_label,
            vdi.name_label as vdi_name_label,
            vdi.uuid as vdi_uuid,
            vdi.vbd_device as vbd_device,
            storages.name_label,
            storages.uuid as sr_uuid
            FROM vdi 
            JOIN vm ON vdi.vm = vm.id 
            JOIN storages ON vdi.storage = storages.id 
            WHERE vdi.snapshot="False" AND vm.version={version}
            ORDER BY `vm_name_label` ASC;
            """)
        return versions

    def get_snapshots(self, version: int) -> list:
        """
        Get all snapshots from specific saved version
        """
        versions = self._fetch_all(f"""
            SELECT 
            vm.uuid as vm_uuid,
            vm.name_label as vm_name_label,
            vm.snapshot_of as vm_uuid_snaphost_of,
            vdi.name_label as vdi_name_label,
            vdi.uuid as vdi_uuid,
            vdi.vbd_device as vbd_device,
            storages.name_label,
            storages.uuid as sr_uuid
            FROM vdi 
            JOIN vm ON vdi.vm = vm.id 
            JOIN storages ON vdi.storage = storages.id 
            WHERE vdi.snapshot="True" AND vm.version={version}
            ORDER BY `vm_name_label` ASC;
            """)
        return versions

    def _fetch_all(self, command: str) -> list:
        """
        Fetch all rows. Return list of tuples.
        :return: list
        """
        my_cursor = self._mydb.cursor()
        my_cursor.execute(command)
        data = my_cursor.fetchall()
        my_cursor.close()
        return data
