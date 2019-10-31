from framework.base.base_element import BaseElement
from framework.enums.web_element_attributes import WebElementAttributes
from framework.utils.regex_utils import fetch_by_regex_first_group


class Photo(BaseElement):
    def __init__(self, by, loc, name):
        super().__init__(by, loc, name)

    @property
    def link_to_download(self):
        return fetch_by_regex_first_group("http.+\\.(jpg|png)", self.style)

    @property
    def style(self):
        return super().web_element.get_attribute(WebElementAttributes.STYLE.value)
