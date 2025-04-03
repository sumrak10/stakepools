from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Body

from src.application.transport.auth.jwt import TokensPairDTO
from src.application.transport.users.users import UserDTO, UserLoginDTO
from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.auth.jwt import JWTAuthUseCase
from src.utils.exceptions import http_exc

router = APIRouter()


@router.post(
    path="/jwt/access",
    response_model=TokensPairDTO,
    responses={
        **http_exc.UnauthorizedHTTPException.docs()
    },
)
async def login(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    dto: UserLoginDTO,
):
    return await JWTAuthUseCase.login(uow, dto)


@router.post(
    path="/jwt/refresh",
    responses={
    },
)
async def refresh(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    refresh_token: str = Body(...),
):
    return await JWTAuthUseCase.refresh(uow, refresh_token)
