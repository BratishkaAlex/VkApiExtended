from selenium.webdriver.common.by import By

from app.enums.side_bar_items import SideBarItems
from framework.elements.button import Button
from framework.utils.logger import info


class SideBar:
    def navigate_to(self, item: SideBarItems):
        info(f"Go to the side bar item with id '{item.value}'")
        self.get_side_bar_item(item).click()

    def get_side_bar_item(self, item: SideBarItems) -> Button:
        return Button(By.ID, item.value, f"Navigate to side bar item with id '{item.value}'")
