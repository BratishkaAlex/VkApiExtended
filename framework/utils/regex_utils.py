import re


def fetch_by_regex_first_group(pattern, string):
    return re.search(pattern, string).group(0)
