from ensurepip import version
from src.Config import LoadConfig
from src.MySQL.MySQL import MySQL

class VDIMySQL(MySQL):

    def __init__(self, config: LoadConfig) -> None:
        super().__init__(config)

    def get_versions(self) -> list:
        """
        Get all versions
        """
        versions = self._fetch_all(f"""
            SELECT * FROM `version` ORDER BY id DESC
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

