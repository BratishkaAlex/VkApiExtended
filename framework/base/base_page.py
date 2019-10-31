from selenium.webdriver.common.by import By

from framework.base.base_element import BaseElement
from framework.utils.logger import info


class BasePage:
    def __init__(self, locator_type: By, locator: str):
        self.__locator_type = locator_type
        self.__locator = locator
        self.__name = type(self).__name__.lower()

    def is_page_opened(self) -> bool:
        info(f"Checking that {self.__name} was opened")
        return BaseElement(self.__locator_type, self.__locator, self.__name).is_displayed()
