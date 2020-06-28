import logging
import sys

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from web.framework.config_parser import Config
from web.framework.patch_webdriver import PatchWebDriver

config = Config()


class DriverHandler:
    __driver = None

    @classmethod
    def get_driver(cls, browser=None):
        if (cls.__driver is None) and (browser is not None):
            cls.__driver = cls.get_local_driver(browser)
            cls.__driver = PatchWebDriver.patch(cls.__driver)
            cls.__driver.maximize_window()
        return cls.__driver

    @classmethod
    def reset_browser(cls):
        cls.__driver = None

    @classmethod
    def quit_browser(cls):
        cls.__driver.quit()
        cls.__driver = None

    @classmethod
    def quit(cls):
        cls.__driver.quit()
        cls.reset_browser()

    @staticmethod
    def get_local_driver(browser_name):
        browser_name = browser_name.lower()
        path = config.get_path_to_local_webdriver(browser_name)

        try:
            if browser_name == 'firefox':
                driver = webdriver.Firefox(executable_path=path)
            elif browser_name == 'chrome':
                driver = webdriver.Chrome(executable_path=path)
            elif browser_name == 'safari':
                caps = DesiredCapabilities().SAFARI
                caps["pageLoadStrategy"] = "normal"
                driver = webdriver.Safari(desired_capabilities=caps)
            else:
                sys.exit("Browser type incorrectly defined")
        except Exception as e:
            logging.error(e)
            raise e
        driver.maximize_window()
        return driver
