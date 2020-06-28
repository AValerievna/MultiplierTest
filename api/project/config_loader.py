from __future__ import annotations

import configparser
import os
from typing import Optional

from .. import definitions

root_dir = definitions.ROOT_DIR
config = configparser.ConfigParser()
config.read(root_dir + '/config.ini')

RUN_TYPE = os.getenv("RUN_TYPE")


class ConfigMeta(type):
    _instance: Optional[Config] = None

    def __call__(cls) -> Config:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Config(metaclass=ConfigMeta):

    host_api = config["hosts"]["API"]
    port_api = config["ports"]["API"]
