import sys, os
import mysql.connector
from src.Config import LoadConfig


class MySQL:
    """ Mysql class """

    def __init__(self, config: LoadConfig) -> None:
        """
        :param config: instanceof LoadConfig
        :return
        """
        self.__mysql = config.get_mysql()
        try:
            self.__mydb = mysql.connector.connect(
                host=self.__mysql['host'],
                user=self.__mysql['user'],
                passwd=self.__mysql['passwd'],
                database=self.__mysql['database']
            )
        except mysql.connector.Error as err:
            print(err)
            print("Error Code: ", err.errno)
            print("SQLSTATE: ", err.sqlstate)
            print("Message: ", err.msg)
            sys.exit(os.EX_UNAVAILABLE)

    # def get_sr_list(self) -> list:
    #     """
    #     Get all SR list
    #     :return: list
    #     """
    #     my_cursor = self.__mydb.cursor()
    #     my_cursor.execute("""
    #         SELECT * FROM `sr-list`
    #         ORDER BY
    #         uid ASC
    #         """)
    #     return my_cursor.fetchall()
    
    def get_sr_by_uuid(self, uuid: str) -> list | None:
        """
        Get one SR by UUID
        :return: list
        """
        my_cursor = self.__mydb.cursor()
        my_cursor.execute("""
            SELECT * FROM `sr-list`
            WHERE `sr-uuid` LIKE '""" + uuid + """'
            """)
        return my_cursor.fetchone()

    def add_new_sr(self, sr_uuid: str, name_label: str, name_description: str) -> None:
        """
        Add new SR
        :return: None
        """
        my_cursor = self.__mydb.cursor()
        my_cursor.execute("""
            INSERT INTO `sr-list`
            (`uid`, `sr-uuid`, `name-label`, `name-description`, `created`)
            VALUES
            (NULL, '""" + sr_uuid + """', '""" + name_label + """', '""" + name_description + """', NOW());
            """)
        self.__mydb.commit()
        my_cursor.close()

    def update_sr(self, sr_uuid: str, name_label: str, name_description: str) -> None:
        """
        Update existing SR
        :return: None
        """
        my_cursor = self.__mydb.cursor()
        my_cursor.execute("""
            UPDATE `sr-list`
            SET `name-label` = '""" + name_label + """' , `name-description` = '""" + name_description + """'
            WHERE `sr-uuid` = '""" + sr_uuid + """'
            """)
        self.__mydb.commit()
        my_cursor.close()
