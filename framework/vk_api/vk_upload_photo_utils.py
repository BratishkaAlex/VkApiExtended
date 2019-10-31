from os.path import abspath

from framework.models.post_request import PostRequest
from framework.vk_api.enums.vk_upload_photos_methods import VkUploadPhotosMethod
from framework.vk_api.models.vk_api_request import VkApiRequest
from resources import vk_config


def get_wall_upload_server_for_photos(access_token):
    parameters = {
        "access_token": access_token,
        "v": vk_config.API_VERSION
    }
    return VkApiRequest(VkUploadPhotosMethod.GET_WALL_UPLOAD_SERVER, parameters).request_result["response"][
        "upload_url"]


def get_uploaded_photo_attributes(photo_name, access_token):
    files = {
        "photo": open(abspath(photo_name), "rb")
    }
    request_result = PostRequest(get_wall_upload_server_for_photos(access_token), None, files=files).request_result
    return request_result["server"], request_result["photo"], request_result["hash"]


def upload_wall_photo(photo_name, access_token):
    server, photo, photo_hash = get_uploaded_photo_attributes(photo_name, access_token)
    parameters = {
        "access_token": access_token,
        "v": vk_config.API_VERSION,
        "server": server,
        "photo": photo,
        "hash": photo_hash
    }
    request_result = VkApiRequest(VkUploadPhotosMethod.SAVE_WALL_PHOTO, parameters).request_result
    return str(request_result["response"][0]["owner_id"]) + "_" + str(request_result["response"][0]["id"])
