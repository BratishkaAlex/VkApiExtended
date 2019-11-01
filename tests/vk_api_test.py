import os

import pytest

from app.enums.side_bar_items import SideBarItems
from app.page_object.pages.my_page import MyPage
from app.page_object.pages.news_page import NewsPage
from app.page_object.pages.unauthorized_page import UnauthorizedPage
from app.steps.steps import log_in, log_out, is_post_deleted, wait_while_entering_captcha, is_doc_uploaded, \
    is_photo_uploaded
from framework.browser.browser import Browser
from framework.utils.logger import Step
from framework.utils.random_utils import get_random_string
from framework.vk_api.enums.vk_attachments_types import VkAttachmentsTypes
from framework.vk_api.enums.vk_items import VkItems
from framework.vk_api.vk_api_utils import create_new_post_with_attachment, is_item_liked_by_user, add_comment_to_post, \
    delete_post, edit_post_and_attach_file, create_new_post
from resources import config, vk_config


class TestVkApi:
    browser = Browser()

    def setup_class(self):
        self.browser.maximize()
        self.browser.set_implicitly_wait(config.TIMEOUT)

    def setup_method(self):
        Step.steps_counter = 1
        if os.path.exists(config.PATH_TO_DOWNLOAD_JPG_PICTURE):
            os.remove(config.PATH_TO_DOWNLOAD_JPG_PICTURE)
        if os.path.exists(config.PATH_TO_DOWNLOAD_PNG_PICTURE):
            os.remove(config.PATH_TO_DOWNLOAD_PNG_PICTURE)
        with Step(f"Go to {config.URL}"):
            self.browser.enter_url(config.URL)
            unauthorized_page = UnauthorizedPage()
            assert unauthorized_page.is_page_opened(), "Unauthorized_page wasn't opened"

    def teardown_method(self):
        log_out()

    def teardown_class(self):
        self.browser.close()

    def test_vk_case_1(self):
        with Step("Authorize as User_1"):
            log_in(vk_config.LOGIN_1, vk_config.PASSWORD_1)
            news_page = NewsPage()
            assert news_page.is_page_opened(), "News page wasn't opened"

        with Step("Go to my page"):
            news_page.side_bar.navigate_to(SideBarItems.MY_PAGE)
            my_page = MyPage()
            assert my_page.is_page_opened(), "My page wasn't opened"

        with Step("Creating post with random line and getting post's id"):
            random_string = get_random_string()
            owner_id = my_page.header.owner_id
            post_id = create_new_post(random_string, vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_post_displayed(post_id, owner_id, random_string), "Post wasn't published"

        with Step("Editing post and upload picture"):
            edited_random_string = f"edited_{random_string}"
            uploaded_photo_id = edit_post_and_attach_file(edited_random_string, VkAttachmentsTypes.PHOTO, post_id,
                                                          config.PATH_TO_JPG_PICTURE,
                                                          vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_post_displayed(post_id, owner_id, edited_random_string) and is_photo_uploaded(
                uploaded_photo_id, config.PATH_TO_JPG_PICTURE,
                config.PATH_TO_DOWNLOAD_JPG_PICTURE), "Post wasn't edited"

        with Step("Adding random comment to the post"):
            random_comment = get_random_string()
            add_comment_to_post(random_comment, post_id, vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_comment_added(owner_id, random_comment), "Comment wasn't added"

        with Step("Like edited post"):
            my_page.post_form.like_post(post_id)
            assert is_item_liked_by_user(VkItems.POST, post_id, owner_id, vk_config.ACCESS_TOKEN_1), "Post wasn't liked"

        with Step("Delete created post"):
            delete_post(post_id, vk_config.ACCESS_TOKEN_1)
            assert is_post_deleted(post_id), "Post wasn't deleted"

    def test_vk_case_2(self):
        with Step("Authorize as User_1"):
            log_in(vk_config.LOGIN_1, vk_config.PASSWORD_1)
            news_page = NewsPage()
            assert news_page.is_page_opened(), "News page wasn't opened"

        with Step("Go to my page"):
            news_page.side_bar.navigate_to(SideBarItems.MY_PAGE)
            my_page = MyPage()
            assert my_page.is_page_opened(), "My page wasn't opened"

        with Step("Creating post with random line and getting post's id"):
            random_string = get_random_string()
            first_user_page_url = self.browser.get_current_url()
            first_user_id = my_page.header.owner_id
            post_id = create_new_post(random_string, vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_post_displayed(post_id, first_user_id, random_string), "Post wasn't published"

        with Step("Like created post as User_1"):
            my_page.post_form.like_post(post_id)

        with Step("Log out"):
            log_out()

        with Step(f"Go to {config.URL}"):
            self.browser.enter_url(config.URL)
            unauthorized_page = UnauthorizedPage()
            assert unauthorized_page.is_page_opened(), "Unauthorized_page wasn't opened"

        with Step("Authorize as User_1"):
            log_in(vk_config.LOGIN_2, vk_config.PASSWORD_2)
            news_page_for_second_user = NewsPage()
            assert news_page_for_second_user.is_page_opened(), "News page for second user wasn't opened"

        with Step(f"Go to {first_user_page_url}"):
            self.browser.enter_url(first_user_page_url)
            assert my_page.is_page_opened(), "Main page for first user wasn't opened"
            second_user_id = my_page.header.owner_id

        with Step(f"Check that created post is on the first user's page"):
            assert my_page.post_form.is_post_displayed(post_id, first_user_id, random_string), "Created post is absent"

        with Step("Like post by User_2"):
            my_page.post_form.like_post(post_id)
            wait_while_entering_captcha()

        with Step("Check that post was liked by User_1 and User_2"):
            assert is_item_liked_by_user(VkItems.POST, post_id, first_user_id,
                                         vk_config.ACCESS_TOKEN_1) and is_item_liked_by_user(
                VkItems.POST, post_id, second_user_id, vk_config.ACCESS_TOKEN_1), "Post wasn't liked by Users"

    def test_vk_case_3(self):
        with Step("Authorize as User_1"):
            log_in(vk_config.LOGIN_1, vk_config.PASSWORD_1)
            news_page = NewsPage()
            assert news_page.is_page_opened(), "News page wasn't opened"

        with Step("Go to my page"):
            news_page.side_bar.navigate_to(SideBarItems.MY_PAGE)
            my_page = MyPage()
            assert my_page.is_page_opened(), "My page wasn't opened"

        with Step("Creating post with random line and getting post's id"):
            random_string = get_random_string()
            user_page_url = self.browser.get_current_url()
            user_id = my_page.header.owner_id
            post_id = create_new_post(random_string, vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_post_displayed(post_id, user_id, random_string), "Post wasn't published"

        with Step("Log out"):
            log_out()

        with Step(f"Go to {config.URL}"):
            self.browser.enter_url(config.URL)
            unauthorized_page = UnauthorizedPage()
            assert unauthorized_page.is_page_opened(), "Unauthorized_page wasn't opened"

        with Step(f"Go to {user_page_url}"):
            self.browser.enter_url(user_page_url)
            assert my_page.is_page_opened(), "Main page for first user wasn't opened"

        with Step(f"Check that created post is on the user's page"):
            assert my_page.post_form.is_post_displayed(post_id, user_id, random_string), "Created post is absent"

    def test_vk_case_4(self):
        with Step("Authorize as User_1"):
            log_in(vk_config.LOGIN_1, vk_config.PASSWORD_1)
            news_page = NewsPage()
            assert news_page.is_page_opened(), "News page wasn't opened"

        with Step("Navigate to my page"):
            news_page.side_bar.navigate_to(SideBarItems.MY_PAGE)
            my_page = MyPage()
            assert my_page.is_page_opened(), "My page wasn't opened"

        with Step("Creating post with random line and getting post's id"):
            random_string = get_random_string()
            owner_id = my_page.header.owner_id
            post_id = create_new_post(random_string, vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_post_displayed(post_id, owner_id, random_string), "Post wasn't published"

        with Step("Editing post with random line and uploading doc"):
            edited_message = f"edited_{random_string}"
            edit_post_and_attach_file(edited_message, VkAttachmentsTypes.DOC, post_id, config.PATH_TO_FILE,
                                      vk_config.ACCESS_TOKEN_1)

        with Step("Check that post was edited"):
            assert my_page.post_form.is_post_displayed(post_id, owner_id, edited_message) \
                   and is_doc_uploaded(post_id, config.PATH_TO_FILE), "Post wasn't edited"

        with Step("Adding random comment to the post"):
            random_comment = get_random_string()
            add_comment_to_post(random_comment, post_id, vk_config.ACCESS_TOKEN_1)
            assert my_page.post_form.is_comment_added(owner_id, random_comment), "Comment wasn't added"

        with Step("Like edited post"):
            my_page.post_form.like_post(post_id)
            assert is_item_liked_by_user(VkItems.POST, post_id, owner_id, vk_config.ACCESS_TOKEN_1), "Post wasn't liked"

        with Step("Delete created post"):
            delete_post(post_id, vk_config.ACCESS_TOKEN_1)
            assert is_post_deleted(post_id), "Post wasn't deleted"

    def idfn(val):
        return "params: {0}".format(str(val))

    @pytest.fixture(scope="function", params=[
        (config.PATH_TO_JPG_PICTURE, config.PATH_TO_DOWNLOAD_JPG_PICTURE),
        (config.PATH_TO_PNG_PICTURE, config.PATH_TO_DOWNLOAD_PNG_PICTURE),
    ], ids=idfn)
    def parameters_for_case_5(self, request):
        return request.param

    def test_vk_case_5(self, parameters_for_case_5):
        path_to_picture, path_to_downloaded_picture = parameters_for_case_5
        with Step("Authorize as User_2"):
            log_in(vk_config.LOGIN_2, vk_config.PASSWORD_2)
            news_page = NewsPage()
            assert news_page.is_page_opened(), "News page wasn't opened"

        with Step("Navigate to my page"):
            news_page.side_bar.navigate_to(SideBarItems.MY_PAGE)
            my_page = MyPage()
            assert my_page.is_page_opened(), "My page wasn't opened"

        with Step("Creating post with random line and photo and getting post's id"):
            random_string = get_random_string()
            owner_id = my_page.header.owner_id
            post_id, uploaded_photo_id = create_new_post_with_attachment(random_string, VkAttachmentsTypes.PHOTO,
                                                                         path_to_picture,
                                                                         vk_config.ACCESS_TOKEN_2)
            assert my_page.post_form.is_post_displayed(post_id, owner_id, random_string) and is_photo_uploaded(
                uploaded_photo_id, path_to_picture,
                path_to_downloaded_picture), "Post wasn't created"
