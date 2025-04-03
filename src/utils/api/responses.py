from typing import Any
from typing import ClassVar

from fastapi import status
from fastapi.responses import JSONResponse


class AbstractCRUDResponse:
    status_code = None
    _description = None
    _message = None
    _detail = None
    _headers = None

    @classmethod
    def response(cls: type["AbstractCRUDResponse"],
                 _message: str | None = None,
                 *,
                 _detail: str | dict | None = None,
                 _headers: dict[str, str] | None = None,
                 ) -> JSONResponse:
        headers = cls._headers or {}
        if _headers is not None:
            headers.update(_headers)
        return JSONResponse(
            content=cls._response_model(_message, _detail=_detail),
            status_code=cls.status_code,
            headers=headers)

    @classmethod
    def docs(cls: type["AbstractCRUDResponse"],
             _message: str | None = None,
             *,
             _detail: str | dict | None = None,
             _description: str | None = None,
             ) -> dict[int | str, dict[str, Any]] | None:
        return {
            cls.status_code: {
                "description": _description or cls._description,
                "content": {
                    "application/json": {
                        "example": cls._response_model(_message, _detail=_detail),
                    },
                },
            },
        }

    @classmethod
    def _response_model(cls: type["AbstractCRUDResponse"],
                        _message: str | None = None,
                        *,
                        _detail: str | dict | None = None,
                        ) -> dict[str, Any]:
        response = {
            "message": _message or cls._message or "OK",
        }
        if _detail is not None or cls._detail is not None:
            response["detail"] = _detail or cls._detail
        return response


class ObjectCreatedResponse(AbstractCRUDResponse):
    status_code = status.HTTP_201_CREATED
    _description = "Returns the ID of the created object as a guarantee of endpoint provisioning."
    _message = "Successfully created"
    _detail: ClassVar[str | dict] = {"id": 0}
    _headers = {'X-Action-Performed': 'create'}


class ObjectUpdatedResponse(AbstractCRUDResponse):
    status_code = status.HTTP_200_OK
    _description = "Successfully updated"
    _message = "Successfully updated"
    _headers = {'X-Action-Performed': 'update'}


class ObjectDeletedResponse(AbstractCRUDResponse):
    status_code = status.HTTP_200_OK
    _description = "Successfully deleted"
    _message = "Successfully deleted"
    _headers = {'X-Action-Performed': 'delete'}
