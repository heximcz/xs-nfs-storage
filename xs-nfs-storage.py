import os
import sys
from src.Config import LoadConfig
from src.Exceptions import ConfigException, XenAPIException
from src.XApiWrapper import XApiWrapper

try:
    config = LoadConfig()
    xs = XApiWrapper(config)
    xs.run()
except ConfigException as e:
    print(e)
    sys.exit(os.EX_UNAVAILABLE)
except XenAPIException as e:
    config.logger.error(e)
    sys.exit(os.EX_UNAVAILABLE)
finally:
    # if (xs.session):
    #     xs.close()
    #     print("Session closed.")
    print("Bye.")