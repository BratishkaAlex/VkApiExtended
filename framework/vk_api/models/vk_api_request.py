from framework.models.post_request import PostRequest


class VkApiRequest(PostRequest):
    def __init__(self, method, parameters):
        super().__init__("https://api.vk.com/method/%s" % method.value, parameters)
