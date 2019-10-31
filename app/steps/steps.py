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


def log_in(login, password):
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
        error("NoSuchElementException")


def is_post_deleted(post_id):
    info("Checking that post was deleted")
    try:
        post_form.get_like_button(post_id).wait_for_element_disappearing()
        return True
    except TimeoutException:
        return False


def is_post_edited_and_photo_uploaded(post_id, owner_id, message, uploaded_photo_id, path_to_picture,
                                      path_to_download_picture):
    info("Checking that post was edited and photo was uploaded")
    download_picture(uploaded_photo_id, path_to_download_picture)
    return compare_two_images_with_accuracy(path_to_picture,
                                            path_to_download_picture) and post_form.is_post_displayed(post_id, owner_id,
                                                                                                      message)


def is_post_edited_and_doc_uploaded(post_id, owner_id, message, path_to_file):
    info("Checking that post was edited and doc was uploaded")
    file_name = os.path.basename(path_to_file)
    return post_form.is_post_displayed(post_id, owner_id, message) and post_form.is_doc_attached_to_post(post_id,
                                                                                                         file_name)


def download_picture(uploaded_photo_id, path_to_download):
    photo = post_form.get_uploaded_photo(uploaded_photo_id)
    download_file(photo.link_to_download, path_to_download)


def wait_while_entering_captcha():
    my_page.skip_validation_button.wait_for_element_disappearing()
    my_page.captcha.wait_for_element_disappearing()
