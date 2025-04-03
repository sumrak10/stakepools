from enum import Enum


class OTPType(Enum):
    REGISTRATION = "REGISTRATION"
    RESET_PASSWORD = "RESET_PASSWORD"
    CHANGE_PASSWORD = "CHANGE_PASSWORD"
    LOGIN = "LOGIN"
