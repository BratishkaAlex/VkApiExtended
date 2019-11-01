from selenium.webdriver.common.by import By

from framework.base.base_element import BaseElement


class InputField(BaseElement):
    def __init__(self, by: By, loc: str, name: str):
        super().__init__(by, loc, name)

    def send_keys(self, text: str):
        super().wait_for_clickable()
        super().web_element.send_keys(text)
