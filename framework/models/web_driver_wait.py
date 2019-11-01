from selenium.webdriver.support.wait import WebDriverWait

from framework.browser.browser import Browser


class DriverWait:
    def __init__(self, timeout: int, poll_frequency: int = 0):
        self.__web_driver_wait = WebDriverWait(Browser().driver, timeout, poll_frequency=poll_frequency)

    @property
    def wait(self) -> WebDriverWait:
        return self.__web_driver_wait
