from __future__ import annotations
from typing import Optional


class HostMeta(type):
    _instance = None

    def __call__(cls) -> Host:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Host(metaclass=HostMeta):
    host = None
