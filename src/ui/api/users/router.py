from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.transport.users.users import (
    UserDTO, UserCreateDTO,
)
from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.auth.jwt import JWTAuthUseCase
from src.application.use_cases.users.users import UsersUseCase
from src.utils.api import responses
from src.utils.exceptions import http_exc

router = APIRouter(
    prefix="/users",
)


@router.get(
    path="/me",
    response_model=UserDTO,
    responses={
        **http_exc.NotFoundHTTPException.docs(),
    },
)
async def get_my_user(
    current_user: Annotated[UserDTO, Depends(JWTAuthUseCase.current_user)],
) -> None:
    return current_user


@router.post(
    path="/register",
    status_code=responses.ObjectCreatedResponse.status_code,
    responses={
        **responses.ObjectCreatedResponse.docs(),
    },
)
async def register(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    create_dto: UserCreateDTO,
):
    user_id = await UsersUseCase.register(uow, create_dto)
    return responses.ObjectCreatedResponse.response(_detail={"id": user_id})

