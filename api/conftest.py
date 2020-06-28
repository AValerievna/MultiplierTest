import pytest

from api.project.api import APIHandler
from api.project.config_loader import Config

config = Config()


@pytest.fixture(scope="session")
def api_handler():
    return APIHandler(host=config.host_api, port=config.port_api)
