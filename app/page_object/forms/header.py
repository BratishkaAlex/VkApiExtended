from selenium.webdriver.common.by import By

from framework.elements.link import Link


class Header:
    @property
    def owner_id(self) -> int:
        top_profile_link = self.top_profile_link.href
        return int(top_profile_link[top_profile_link.rfind("id") + len("id"):])

    @property
    def top_profile_link(self) -> Link:
        return Link(By.ID, "top_profile_link", "Top profile")

    @property
    def logout_button(self) -> Link:
        return Link(By.ID, "top_logout_link", "logout")
