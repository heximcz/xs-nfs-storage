import socket
import XenAPI
from typing import Union, Type
from src.Config import LoadConfig

class XApiConnect:

    def __init__(self, config: LoadConfig) -> None:
        env = config.get_xs()
        self.session: XenAPI.Session = None
        try:
           self.session = XenAPI.Session(env['url'])
           self.session.xenapi.login_with_password(env['login'], env['pwd'], "2.3", "xapi-xs-nfs-storage")
        except ConnectionRefusedError as e:
            config.logger.error("XenAPIConnect URL: " + e.strerror)
            self.session = None
        except XenAPI.XenAPI.Failure as e:
            config.logger.error("XenAPIConnect Authorization: " + str(e))
            self.session = None
        except socket.gaierror as e:
            config.logger.error("XenAPIConnect Domain: " + str(e))
            self.session = None
    
    def close(self):
        self.session.xenapi.session.logout()

