import requests


def download_file(url, path):
    with open(path, "wb") as download_file:
        download_file.write(requests.get(url).content)
