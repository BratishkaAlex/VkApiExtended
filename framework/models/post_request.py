import requests


class PostRequest:
    def __init__(self, url, parameters=None, files=None):
        self.__request_result = requests.post(url, data=parameters, files=files)

    @property
    def request_result(self):
        return self.__request_result.json()
