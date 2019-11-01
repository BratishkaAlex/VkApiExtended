from selenium.webdriver.common.by import By

from framework.elements.button import Button
from framework.elements.label import Label
from framework.elements.link import Link
from framework.elements.photo import Photo
from framework.utils.logger import info


class PostForm:
    def see_comments_under_created_post(self):
        self.button_to_see_comments.click()

    def like_post(self, post_id: int):
        self.get_like_button(post_id).click()

    def is_post_displayed(self, post_id: int, owner_id: int, message: str) -> bool:
        return self.get_post(post_id, owner_id, message).is_displayed()

    def is_comment_added(self, owner_id: int, message: str) -> bool:
        info("Checking that comment was added")
        return self.get_comment(owner_id, message).is_displayed()

    def is_doc_attached_to_post(self, post_id: int, file_name: str) -> bool:
        return self.get_file_link(post_id, file_name).is_displayed()

    def get_uploaded_photo(self, uploaded_photo_id: str) -> Photo:
        return Photo(By.XPATH, f"//a[contains(@href,'{uploaded_photo_id}')]", "Uploaded  photo")

    def get_like_button(self, post_id: int) -> Button:
        return Button(By.XPATH, f"//a[contains(@class,'_like') and contains(@onclick,'{post_id}')]",
                      "Like icon for VK post")

    def get_comment(self, owner_id: int, message: str) -> Label:
        self.see_comments_under_created_post()
        return Label(By.XPATH, f"//a[@class='author' and contains(@href,'{owner_id}')]//..//..//"
                               f"div[@class='wall_reply_text' and text()='{message}']", "Added comment")

    @property
    def button_to_see_comments(self) -> Button:
        return Button(By.CSS_SELECTOR, "a.replies_next_main", "See comments")

    def get_post(self, post_id: int, owner_id: int, message: str) -> Label:
        return Label(By.XPATH,
                     f"//div[contains(@class,'wall_post_text') and text()='{message}'][//div[contains(@data-post-id,"
                     f"'{post_id}')]//a[@class='author' and contains(@href,'{owner_id}')]]", "Created post's text")

    def get_file_link(self, post_id: int, file_name: str) -> Link:
        return Link(By.XPATH, f"//div[contains(@id,'{post_id}')]//a[text()='{file_name}']", "Uploaded doc")
