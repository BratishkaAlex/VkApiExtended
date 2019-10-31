from framework.base.base_element import BaseElement


class InputField(BaseElement):
    def __init__(self, by, loc, name):
        super().__init__(by, loc, name)

    def send_keys(self, text):
        super().wait_for_clickable()
        super().web_element.send_keys(text)
