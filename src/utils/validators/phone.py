import re


def check_for_uzbekistan_phone_format(value: str) -> bool:
    return re.match(r"^\+998\d{9}$", value)
