from __future__ import annotations
from typing import Any

from fastapi import HTTPException
from fastapi import status


class AbstractHttpException(Exception):
    """Abstract class for HTTP exceptions."""

    _status_code = None
    _detail = None
    _description = None
    _headers = None

    def __init__(self, detail: str | dict | None = None, *, headers: dict[str, str] | None = None) -> None:
        if headers is None:
            headers = {}
        self._status_code = self._status_code
        self._detail = detail or self._detail
        self._headers = headers.update(self._headers or {})

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def detail(self) -> str:
        return self._detail

    @property
    def description(self) -> str:
        return self._description

    @classmethod
    def docs(cls: type[AbstractHttpException]) -> dict[int | str, dict[str, Any]] | None:
        return {
            cls._status_code: {
                "description": cls._description,
                "content": {
                    "application/json": {
                        "example": {"detail": cls._detail},
                    },
                },
            },
        }


class UnauthorizedHTTPException(AbstractHttpException):
    _status_code = status.HTTP_401_UNAUTHORIZED
    _detail = "Could not validate credentials."
    _headers = {"WWW-Authenticate": "Bearer"}


class ForbiddenHTTPException(AbstractHttpException):
    _status_code = status.HTTP_403_FORBIDDEN
    _detail = "You don't have enough rights."


class NotFoundHTTPException(AbstractHttpException):
    _status_code = status.HTTP_404_NOT_FOUND
    _detail = "Object not found."


class NotAcceptableHTTPException(AbstractHttpException):
    _status_code = status.HTTP_406_NOT_ACCEPTABLE
    _detail = "Your queries do not meet the required conditions. You will get more details when a real error occurs."


class BadRequestHTTPException(AbstractHttpException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _detail = "Your queries do not meet the required conditions. You will get more details when a real error occurs."


class ImUsedHTTPException(AbstractHttpException):
    _status_code = status.HTTP_226_IM_USED
    _detail = "Im used ;D"


class DoubtfulButOkayHTTPException(AbstractHttpException):
    _status_code = 267
    _detail = "Doubtful but okay (-_-)"


class GatewayTimeoutHTTPException(AbstractHttpException):
    _status_code = status.HTTP_504_GATEWAY_TIMEOUT
    _detail = "Gateway timeout. Please try again later."


class UnprocessableEntityHTTPException(AbstractHttpException):
    _status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    _detail = "Unprocessable entity. Please check the request body."


# Custom cases
class InvalidOTPCodeHTTPException(AbstractHttpException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _detail = "Invalid OTP code or password."


class InvalidPasswordHTTPException(AbstractHttpException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _detail = "Invalid password."


class InvalidOTPCodeOrPasswordHTTPException(AbstractHttpException):
    _status_code = status.HTTP_400_BAD_REQUEST
    _detail = "Invalid OTP code or password."
