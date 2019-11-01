import requests


class PostRequest:
    def __init__(self, url: str, parameters: dict = None, files: dict = None):
        self.__request_result = requests.post(url, data=parameters, files=files)

    @property
    def request_result(self) -> dict:
        return self.__request_result.json()
