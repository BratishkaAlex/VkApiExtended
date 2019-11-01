from selenium.webdriver.common.by import By

from framework.base.base_element import BaseElement
from framework.enums.web_element_attributes import WebElementAttributes


class Link(BaseElement):
    def __init__(self, by: By, loc: str, name: str):
        super().__init__(by, loc, name)

    @property
    def href(self) -> str:
        return super().get_attribute(WebElementAttributes.HREF)
