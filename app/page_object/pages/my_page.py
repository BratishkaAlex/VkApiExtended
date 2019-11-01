from selenium.webdriver.common.by import By

from app.page_object.forms.header import Header
from app.page_object.forms.post_form import PostForm
from framework.base.base_page import BasePage
from framework.elements.button import Button
from framework.elements.photo import Photo


class MyPage(BasePage):
    def __init__(self):
        super().__init__(By.ID, "page_info_wrap")
        self.__post_form = PostForm()
        self.__header = Header()

    @property
    def post_form(self) -> PostForm:
        return self.__post_form

    @property
    def header(self) -> Header:
        return self.__header

    @property
    def skip_validation_button(self) -> Button:
        return Button(By.ID, "validation_skip", "skip_phone_validation")

    @property
    def captcha(self) -> Photo:
        return Photo(By.CSS_SELECTOR, ".captcha", "Captcha")
