from selenium.webdriver.support import expected_conditions

from framework.browser.browser import Browser
from framework.models.web_driver_wait import DriverWait
from framework.utils.logger import debug
from resources import config

browser = Browser()


class BaseElement:
    def __init__(self, by, loc, name):
        self.__by = by
        self.__loc = loc
        self.__name = f"{type(self).__name__}, '{name}'"
        debug(f"Creating instance of {self.__name}")

    def is_displayed(self):
        return self.web_element.is_displayed()

    def click(self):
        self.web_element.click()

    def wait_and_click(self):
        self.wait_for_clickable()
        self.web_element.click()

    def get_attribute(self, attribute):
        return self.web_element.get_attribute(attribute)

    def get_text(self):
        return self.web_element.text

    def wait_for_clickable(self):
        DriverWait(config.TIMEOUT).wait.until(
            expected_conditions.element_to_be_clickable((self.by, self.loc)))

    def wait_for_element_presence(self):
        DriverWait(config.TIMEOUT).wait.until(
            expected_conditions.presence_of_element_located((self.by, self.loc)))

    def wait_for_element_disappearing(self):
        DriverWait(config.TIMEOUT_FOR_CAPTCHA).wait.until(
            expected_conditions.invisibility_of_element_located((self.by, self.loc)))

    @property
    def web_element(self):
        return browser.driver.find_element(self.by, self.loc)

    @property
    def by(self):
        return self.__by

    @property
    def loc(self):
        return self.__loc
