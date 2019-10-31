from framework.utils.logger import info
from framework.vk_api.enums.vk_attachments_types import VkAttachmentsTypes
from framework.vk_api.enums.vk_like_methods import VkLikeMethods
from framework.vk_api.enums.vk_wall_methods import VkWallMethods
from framework.vk_api.vk_upload_files_utils import save_file
from framework.vk_api.vk_upload_photo_utils import *
from resources import vk_config


def create_new_post(message, access_token):
    parameters = {
        "access_token": access_token,
        "message": message,
        "v": vk_config.API_VERSION
    }
    return int(VkApiRequest(VkWallMethods.POST, parameters).request_result["response"]["post_id"])


def create_new_post_with_attachment(message, attachment_type: VkAttachmentsTypes, file, access_token):
    post_id = create_new_post(message, access_token)
    attachment_id = edit_post_and_attach_file(message, attachment_type, post_id, file, access_token)
    return post_id, attachment_id


def edit_post_and_attach_file(message, attachment_type: VkAttachmentsTypes, post_id, file, access_token):
    file_id = ""
    if attachment_type is VkAttachmentsTypes.PHOTO:
        file_id = upload_wall_photo(file, access_token)
    elif attachment_type is VkAttachmentsTypes.DOC:
        file_id = save_file(file, access_token)
    parameters = {
        "access_token": access_token,
        "post_id": post_id,
        "message": message,
        "v": vk_config.API_VERSION,
        "attachments": f"{attachment_type.value}{file_id}"
    }
    VkApiRequest(VkWallMethods.EDIT, parameters)
    return file_id


def add_comment_to_post(message, post_id, access_token):
    parameters = {
        "access_token": access_token,
        "post_id": post_id,
        "message": message,
        "v": vk_config.API_VERSION
    }
    VkApiRequest(VkWallMethods.CREATE_COMMENT, parameters)


def is_item_liked_by_user(item_type, post_id, user_id, access_token):
    info(f"Checking that post was liked by user with id {user_id}")
    parameters = {
        "access_token": access_token,
        "type": item_type.value,
        "item_id": post_id,
        "user_id": user_id,
        "v": vk_config.API_VERSION
    }
    return VkApiRequest(VkLikeMethods.IS_LIKED, parameters).request_result["response"]["liked"] == 1


def delete_post(post_id, access_token):
    parameters = {
        "access_token": access_token,
        "post_id": post_id,
        "v": vk_config.API_VERSION
    }
    VkApiRequest(VkWallMethods.DELETE, parameters)
