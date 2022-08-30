import os
import sys
import fire
from src.Config import LoadConfig
from src.Exceptions import ConfigException, XenAPIException
from src.XApi.XApiWrapper import XApiWrapper

try:
    config = LoadConfig()
    xs = XApiWrapper(config)
except ConfigException as e:
    print(e)
    sys.exit(os.EX_UNAVAILABLE)
except XenAPIException as e:
    config.logger.error(e)
    sys.exit(os.EX_UNAVAILABLE)

if __name__ == '__main__':
    fire.Fire(xs)
