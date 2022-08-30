import socket
import XenAPI
from src.Config import LoadConfig

class XApiConnect:

    def __init__(self, config: LoadConfig) -> None:
        self.__env = config.get_xs()
        self.__config = config
        self.session: XenAPI.Session = None

    def open(self):
        """
        XAPI open connection
        """
        try:
           self.session = XenAPI.Session(self.__env['url'])
           self.session.xenapi.login_with_password(self.__env['login'], self.__env['pwd'], "2.3", "xapi-xs-nfs-storage")
        except ConnectionRefusedError as e:
            self.__config.logger.error("XenAPIConnect URL: " + e.strerror)
            self.session = None
        except XenAPI.XenAPI.Failure as e:
            self.__config.logger.error("XenAPIConnect Authorization: " + str(e))
            self.session = None
        except socket.gaierror as e:
            self.__config.logger.error("XenAPIConnect Domain: " + str(e))
            self.session = None

    def close(self):
        """
        XAPI close connection
        """
        self.session.xenapi.session.logout()

