from selenium.webdriver.common.by import By

from app.page_object.forms.side_bar import SideBar
from framework.base.base_page import BasePage


class NewsPage(BasePage):
    def __init__(self):
        super().__init__(By.ID, "submit_post_box")
        self.__side_bar = SideBar()

    @property
    def side_bar(self):
        return self.__side_bar
