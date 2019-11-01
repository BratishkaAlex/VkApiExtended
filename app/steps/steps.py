import os

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from app.page_object.forms.header import Header
from app.page_object.forms.post_form import PostForm
from app.page_object.pages.my_page import MyPage
from app.page_object.pages.unauthorized_page import UnauthorizedPage
from framework.utils.comparison_utils import compare_two_images_with_accuracy
from framework.utils.download_utils import download_file
from framework.utils.logger import info, error

unauthorized_page = UnauthorizedPage()
post_form = PostForm()
header = Header()
my_page = MyPage()


def log_in(login: str, password: str):
    info("Authorize")
    unauthorized_page.type_login(login)
    unauthorized_page.type_password(password)
    unauthorized_page.click_submit()


def log_out():
    try:
        if header.top_profile_link.is_displayed():
            header.top_profile_link.click()
            header.logout_button.click()
    except NoSuchElementException:
        error("User already logged out")


def is_post_deleted(post_id: int) -> bool:
    info("Checking that post was deleted")
    try:
        post_form.get_like_button(post_id).wait_for_element_disappearing()
        return True
    except TimeoutException:
        return False


def is_photo_uploaded(uploaded_photo_id: str, path_to_picture: str, path_to_download_picture: str) -> bool:
    info("Checking that photo was uploaded in post")
    download_picture(uploaded_photo_id, path_to_download_picture)
    return compare_two_images_with_accuracy(path_to_picture,
                                            path_to_download_picture)


def is_doc_uploaded(post_id: int, path_to_file: str) -> bool:
    info("Checking that doc was uploaded to post")
    file_name = os.path.basename(path_to_file)
    return post_form.is_doc_attached_to_post(post_id, file_name)


def download_picture(uploaded_photo_id: str, path_to_download: str):
    photo = post_form.get_uploaded_photo(uploaded_photo_id)
    download_file(photo.link_to_download, path_to_download)


def wait_while_entering_captcha():
    my_page.skip_validation_button.wait_for_element_disappearing()
    my_page.captcha.wait_for_element_disappearing()
