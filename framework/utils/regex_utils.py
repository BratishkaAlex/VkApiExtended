import re


def fetch_by_regex_first_group(pattern: str, string: str) -> str:
    return re.search(pattern, string).group(0)
