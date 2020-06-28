from __future__ import annotations
from typing import Optional

import logging
import configparser
import os.path
import sys
import os

from web import definitions

core_dir = definitions.ROOT_DIR
app_dir = os.path.dirname(core_dir)
logging.info("core_dir = " + str(core_dir))

config = configparser.ConfigParser()
config.read(core_dir + '/config.ini')


class ConfigMeta(type):
    _instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Config(metaclass=ConfigMeta):

    @property
    def url_selenium_hub(self):
        return os.getenv("HOST_HUB")

    @staticmethod
    def get_path_to_local_webdriver(driver_type):
        platform = sys.platform
        try:
            if platform =='darwin':
                return app_dir + config[platform][driver_type]
            elif platform =='linux':
                return app_dir + config[platform][driver_type]
            else:
                raise NameError("Failed to use the type of OS system")
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_host_by_env(env):
        return config["host"][env]
