import yaml
import logging
import logging.config
from pathlib import PurePath
from src.Exceptions import ConfigException

class LoadConfig:
    """ environment and logging """

    def __init__(self):

        self.__config: dict[any, any]
        self.logger: object = None

        # load logger
        logging.config.dictConfig(self.__get_config('../../logger.yml'))
        self.logger = logging.getLogger(__name__)

        # load config
        self.__config = self.__get_config('../../config.yml')

    def env(self, env: str) -> str:
        """
        Get one value by name from config file
        :param env: str
        :return: string
        """
        return self.__config[env]

    def get_mysql(self) -> dict[any, any]:
        """
        Get mysql connector config
        :return: list
        """
        return self.__config['mysql']

    def get_xs(self) -> dict[any, any]:
        """
        Get XenServer (XCP-NG) API login config
        :return: list
        """
        return self.__config['xs']

    def __get_config(self, file: str) -> dict[any, any]:
        """
        Load data from yaml file
        :param file: str
        :return: list
        """
        try:
            file_path = PurePath(__file__).parent.joinpath(file)
            with open(file_path, 'r') as stream:
                try:
                    return yaml.load(stream, Loader=yaml.SafeLoader)
                except yaml.YAMLError:
                    raise ConfigException('Syntax error in a yaml file: ' + file)
        except FileNotFoundError:
            raise ConfigException('No such file or directory: ' + file)
