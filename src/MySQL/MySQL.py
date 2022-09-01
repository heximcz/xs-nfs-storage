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
            self._mydb = mysql.connector.connect(
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
