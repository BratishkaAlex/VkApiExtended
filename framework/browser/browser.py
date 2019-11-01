from selenium import webdriver

from framework.browser.browser_factory import get_driver
from framework.models.singleton import Singleton
from framework.utils.logger import debug


class Browser(metaclass=Singleton):
    def __init__(self):
        self.__driver = get_driver()

    @property
    def driver(self) -> webdriver:
        return self.__driver

    def maximize(self):
        debug("Maximize browser window")
        self.driver.maximize_window()

    def enter_url(self, url: str):
        debug(f"Entering {url}")
        self.driver.get(url)

    def close(self):
        debug("Close browser")
        self.driver.quit()

    def get_current_url(self) -> str:
        debug("Get current browser")
        return self.driver.current_url

    def set_implicitly_wait(self, timeout: int):
        self.driver.implicitly_wait(timeout)
