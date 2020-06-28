from web.framework.base_page import BasePage


class MainPage(BasePage):

    FIRST_INPUT = "//body//input[1]"
    SECOND_INPUT = "//body//input[2]"
    MULTPLAY_BTN = "//button[@id='submit_btn']"
    CALCUTATION_TITLE = "//h3[contains(text(),'Calculator')]"
    RESULT_FIELD = "//div[@id='result']"
    INTERFACE_CONTAINER = "//div[@class='container']"
    INTERFACE_LINE = "//div[@class='container']//hr"
    FIRST_ERROR_TICKER = "/preceding-sibling::span[@class='error-text']"
    SECOND_ERROR_TICKER = "/following-sibling::span[@class='error-text']"

    def is_content_displayed(self):
        return all([self.is_visible_element_with_xpath(xpath=self.INTERFACE_CONTAINER),
                    self.is_visible_element_with_xpath(xpath=self.CALCUTATION_TITLE),
                    self.is_visible_element_with_xpath(xpath=self.FIRST_INPUT),
                    self.is_visible_element_with_xpath(xpath=self.SECOND_INPUT),
                    self.is_visible_element_with_xpath(xpath=self.INTERFACE_LINE),
                    self.is_visible_element_with_xpath(xpath=self.RESULT_FIELD)])

    def input_first_digit(self, first_digit):
        first_input = self.get_clickable_element_with_xpath(xpath=self.FIRST_INPUT)
        first_input.click()
        first_input.send_keys(first_digit)

    def input_second_digit(self, second_digit):
        second_input = self.get_clickable_element_with_xpath(xpath=self.SECOND_INPUT)
        second_input.click()
        second_input.send_keys(second_digit)

    def click_multiply_btn(self):
        mult_btn = self.get_clickable_element_with_xpath(xpath=self.MULTPLAY_BTN)
        mult_btn.click()

    def get_result_after_multiply(self):
        res = "Result:"
        while res == "Result:":
            res = self.get_visible_element_with_xpath(xpath=self.RESULT_FIELD).text
        return res

    def get_first_error_msg(self):
        return self.get_visible_element_with_xpath(xpath=self.SECOND_INPUT + self.FIRST_ERROR_TICKER).text

    def get_second_error_msg(self):
        return self.get_visible_element_with_xpath(xpath=self.SECOND_INPUT + self.SECOND_ERROR_TICKER).text
