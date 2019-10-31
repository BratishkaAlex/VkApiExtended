from selenium.webdriver.common.by import By

from framework.elements.button import Button
from framework.utils.logger import info


class SideBar:
    def navigate_to(self, item):
        info(f"Go to the side bar item with id '{item.value}'")
        self.get_side_bar_item(item).click()

    def get_side_bar_item(self, item):
        return Button(By.ID, item.value, f"Navigate to side bar item with id '{item.value}'")
