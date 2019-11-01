from selenium.webdriver.common.by import By

from framework.base.base_element import BaseElement


class Label(BaseElement):
    def __init__(self, by: By, loc: str, name: str):
        super().__init__(by, loc, name)
