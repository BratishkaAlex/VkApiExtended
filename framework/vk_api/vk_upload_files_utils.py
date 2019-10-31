from os.path import abspath

from framework.models.post_request import PostRequest
from framework.vk_api.enums.vk_upload_file_methods import VkUploadFilesMethod
from framework.vk_api.models.vk_api_request import VkApiRequest
from resources import vk_config


def get_wall_upload_server_for_files(access_token):
    parameters = {
        "access_token": access_token,
        "v": vk_config.API_VERSION
    }
    return VkApiRequest(VkUploadFilesMethod.GET_WALL_UPLOAD_SERVER, parameters).request_result["response"][
        "upload_url"]


def get_uploaded_file_attribute(file, access_token):
    files = {
        "file": open(abspath(file), "rb")
    }
    request_result = PostRequest(get_wall_upload_server_for_files(access_token), files=files).request_result
    return request_result["file"]


def save_file(file, access_token):
    parameters = {
        "access_token": access_token,
        "v": vk_config.API_VERSION,
        "file": get_uploaded_file_attribute(file, access_token),
    }
    request_result = VkApiRequest(VkUploadFilesMethod.SAVE, parameters).request_result
    return str(request_result["response"]["doc"]["owner_id"]) + "_" + str(request_result["response"]["doc"]["id"])
