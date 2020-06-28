from contextlib import contextmanager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions

from web.framework.browser_handler import BrowserHandler
from web.framework.config_parser import Config
from web.framework.init_host import Host
from web.framework.webdriver_handler import DriverHandler

import logging

config = Config()

TIMEOUT_5 = 5


class BasePage:

    def __init__(self, page=""):
        self.host = Host.host
        self.page = page
        self._driver = DriverHandler.get_driver()

    def open(self):
        self._driver.get(self.host + self.page)
        browser = BrowserHandler(webdriver=self._driver)
        browser.page_is_loaded()

    def get_title(self):
        return str(self._driver.title)

    # methods using xpaths
    def get_clickable_element_with_xpath(self, xpath, timeout=TIMEOUT_5):
        try:
            return WebDriverWait(self._driver, timeout).until(
                method=expected_conditions.element_to_be_clickable((By.XPATH, xpath)),
                message="method -> element_to_be_clickable. xpath -> " + xpath)
        except exceptions.TimeoutException as e:
            raise exceptions.NoSuchElementException(msg=e.msg)

    def click_element_with_xpath(self, xpath, timeout=TIMEOUT_5):
        return self.get_clickable_element_with_xpath(xpath=xpath, timeout=timeout).click()

    def input_keys_to_element_with_xpath(self, xpath, input_keys, timeout=TIMEOUT_5):
        return self.get_clickable_element_with_xpath(xpath=xpath, timeout=timeout).send_keys(input_keys)

    def clear_input_to_element_with_xpath(self, xpath, timeout=TIMEOUT_5):
        return self.get_clickable_element_with_xpath(xpath=xpath, timeout=timeout).clear()

    def get_element_attribute_with_xpath(self, xpath, attr, timeout=TIMEOUT_5):
        return self.get_visible_element_with_xpath(xpath=xpath, timeout=timeout).get_attribute(name=attr)

    def get_element_text_with_xpath(self, xpath, timeout=TIMEOUT_5):
        return self.get_visible_element_with_xpath(xpath=xpath, timeout=timeout).text

    def get_visible_element_with_xpath(self, xpath, timeout=TIMEOUT_5):
        try:
            return WebDriverWait(self._driver, timeout).until(
                method=expected_conditions.visibility_of_element_located((By.XPATH, xpath)),
                message="method -> visibility_of_element_located. xpath -> " + xpath)
        except exceptions.TimeoutException as e:
            raise exceptions.NoSuchElementException(msg=e.msg)

    def is_visible_element_with_xpath(self, xpath, timeout=TIMEOUT_5):
        try:
            WebDriverWait(self._driver, timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except exceptions.TimeoutException:
            logging.error(__name__ + " element ->> {xpath} <<- not found".format(xpath=xpath))
            return False

    def get_list_of_elements_with_xpath(self, xpath, timeout=TIMEOUT_5):
        try:
            return WebDriverWait(self._driver, timeout).until(
                method=expected_conditions.presence_of_all_elements_located((By.XPATH, xpath)),
                message="method -> presence_of_all_elements_located. xpath -> " + xpath)
        except exceptions.TimeoutException as e:
            raise exceptions.NoSuchElementException(msg=e.msg)

    #methods using webelements
    def click_element(self, webelem):
        return webelem.click()

    def input_keys_to_element(self, webelem, input_keys):
        return webelem.send_keys(input_keys)

    def clear_input_to_element(self, webelem):
        return webelem.clear()

    def get_element_text(self, webelem):
        return webelem.text

    def get_element_attribute(self, webelem, attr):
        return webelem.get_attribute(name=attr)

    def is_visible_element(self, webelem):
        try:
            return webelem.is_displayed()
        except exceptions.TimeoutException:
            logging.error(__name__ + " element ->> {name} <<- not found".format(name=webelem.__name__))
            return False

    def switch_to_element_frame(self, webelem):
        self._driver.switch_to_frame(frame_reference=webelem)

    def scroll_to_element(self, webelem):
        self._driver.execute_script("arguments[0].scrollIntoView();", webelem)

    @contextmanager
    def wait_for_page_load(self, timeout=4):
        old_page = self._driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self._driver, timeout).until(staleness_of(old_page))
