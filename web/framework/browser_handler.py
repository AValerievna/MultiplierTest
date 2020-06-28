from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import time


class BrowserHandler:

    def __init__(self, webdriver: WebDriver):
        self.webdriver = webdriver
        self.current_active_tab = self.webdriver.current_window_handle

    def __switch_tab(self):
        time.sleep(3)
        if self.get_count_tabs() > 1:
            for a in self.webdriver.window_handles:
                if a != self.current_active_tab:
                    self.webdriver.switch_to.window(a)
                    return

    def get_opened_tab_title(self) -> str:
        self.__switch_tab()
        return self.webdriver.title

    def get_opened_tab_url(self) -> str:
        self.__switch_tab()
        return str(self.webdriver.current_url)

    def get_count_tabs(self) -> int:
        return len(self.webdriver.window_handles)

    def page_is_loaded(self) -> bool:
        self.__switch_tab()
        return WebDriverWait(self.webdriver, 15).until(page_is_ready("complete"))

    def back(self):
        self.webdriver.back()

    def close_tab(self):
        self.__switch_tab()
        self.webdriver.close()
        self.webdriver.switch_to.window(self.current_active_tab)

    def page_is_scrolled(self) -> bool:
        count_pixels = self.webdriver.execute_script("return window.pageYOffset;")
        if count_pixels > 5:
            return True
        else:
            return False

    def scroll_to_element(self, element: WebElement):
        self.webdriver.execute_script("arguments[0].scrollIntoView();", element)


class page_is_ready(object):

    def __init__(self, status):
        self.status = status

    def __call__(self, driver):
        return driver.execute_script("return document.readyState") == self.status
