class OTPException(Exception):
    pass


class DisallowedHost(OTPException):
    """Exception raised when the host is not allowed to access the OTP service."""
    pass
