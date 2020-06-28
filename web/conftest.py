import pytest

from web import definitions
from web.framework.config_parser import Config
from web.framework.init_host import Host
from web.framework.patch_webdriver import PatchWebDriver
from web.framework.webdriver_handler import DriverHandler

config = Config()
ROOT_DIR = definitions.ROOT_DIR


@pytest.yield_fixture(scope="session", autouse=True)
def init_host(request):
    host = request.config.getoption('host')
    Host.host = Config.get_host_by_env(host)


@pytest.yield_fixture(scope="function", autouse=True)
def init_browser(browser) -> PatchWebDriver:
    driver = DriverHandler.get_driver(browser)

    yield driver
    DriverHandler.quit_browser()


@pytest.fixture
def browser(request):
    return request.config.getoption('browser')


@pytest.fixture
def host(request):
    return request.config.getoption('host')


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome', help='Install browser type (Default:Chrome)')
    parser.addoption('--host', default='master')
