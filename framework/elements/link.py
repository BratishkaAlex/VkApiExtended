from framework.base.base_element import BaseElement
from framework.enums.web_element_attributes import WebElementAttributes


class Link(BaseElement):
    def __init__(self, by, loc, name):
        super().__init__(by, loc, name)

    @property
    def href(self):
        return super().web_element.get_attribute(WebElementAttributes.HREF.value)
