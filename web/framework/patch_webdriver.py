from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import exceptions
import logging

TIMEOUT_5 = 5


class PatchWebDriver(WebDriver):

    def __init__(self, orig_driver: WebDriver):
        self.my_driver = orig_driver
        orig_driver.find_element_by_xpath_ww = self.find_element_by_xpath_ww
        orig_driver.find_elements_by_xpath_ww = self.find_elements_by_xpath_ww
        orig_driver.element_is_displayed_by_xpath = self.element_is_displayed_by_xpath
        orig_driver.element_is_displayed_by_webelem = self.element_is_displayed_by_webelem
        orig_driver.scroll_to_element = self.scroll_to_element

    def find_element_by_xpath_ww(self, xpath, timeout=TIMEOUT_5) -> WebElement:
        try:
            WebDriverWait(self.my_driver, timeout).until(
                method=expected_conditions.visibility_of_element_located((By.XPATH, xpath)),
                message="method -> visibility_of_element_located. xpath -> " + xpath)
            WebDriverWait(self.my_driver, timeout).until(
                method=expected_conditions.element_to_be_clickable((By.XPATH, xpath)),
                message="method -> element_to_be_clickable. xpath -> " + xpath)
            return self.my_driver.find_element_by_xpath(xpath)
        except exceptions.TimeoutException as e:
            raise exceptions.NoSuchElementException(msg=e.msg)

    def find_elements_by_xpath_ww(self, xpath, timeout=TIMEOUT_5):
        try:
            WebDriverWait(self.my_driver, timeout).until(
                method=expected_conditions.presence_of_all_elements_located((By.XPATH, xpath)),
                message="method -> presence_of_all_elements_located. xpath -> " + xpath)
            return self.my_driver.find_elements_by_xpath(xpath)
        except exceptions.TimeoutException as e:
            raise exceptions.NoSuchElementException(msg=e.msg)

    def element_is_displayed_by_xpath(self, xpath, timeout=TIMEOUT_5) -> bool:
        try:
            WebDriverWait(self.my_driver, timeout).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath)))
            return True
        except exceptions.TimeoutException:
            logging.error(__name__ + " element ->> {0} <<- not found".format(xpath))
            return False

    def element_is_displayed_by_webelem(self, element: WebElement) -> bool:
        try:
            element.is_displayed()
            return True
        except exceptions.TimeoutException:
            logging.error(__name__ + " element ->> {0} <<- not found".format(element.__name__))
            return False

    def scroll_to_element(self, element: WebElement):
        self.my_driver.execute_script("arguments[0].scrollIntoView();", element)

    @staticmethod
    def patch(driver):
        PatchWebDriver(driver)
        return driver
