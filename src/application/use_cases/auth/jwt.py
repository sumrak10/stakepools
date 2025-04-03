import datetime
from typing import Annotated, Any

import jwt
from fastapi.params import Depends, Header
from starlette.requests import Request

from src.application.transport.auth.jwt import TokensPairDTO
from src.application.transport.users.users import UserLoginDTO, UserDTO
from src.application.uow.uow import IUnitOfWork
from src.config.jwt import jwt_settings
from src.utils.exceptions import http_exc
from src.utils.passwords import PasswordsService


class JWTAuthUseCase:
    @classmethod
    async def login(cls,
                    uow: IUnitOfWork,
                    dto: UserLoginDTO
                    ) -> TokensPairDTO:
        async with uow:
            user = await uow.users.get_one_by_email(dto.email)
            if not PasswordsService.verify_password(
                    dto.password.get_secret_value(),
                    user.password.get_secret_value()
            ):
                raise http_exc.UnauthorizedHTTPException
            await uow.commit()
        return cls._build_tokens_pair(user.id)

    @classmethod
    async def refresh(cls,
                      uow: IUnitOfWork,
                      refresh_token: str,
                      ) -> TokensPairDTO:
        async with uow:
            user_id = cls._validate_token(refresh_token)
            user = await uow.users.get_one_by_id(user_id)
            if not user:
                raise http_exc.UnauthorizedHTTPException
            await uow.commit()
        return cls._build_tokens_pair(user.id)

    @classmethod
    async def current_user(
            cls,
            uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
            x_access_token: str = Header(...),
    ) -> UserDTO | None:
        return await cls.authenticate(uow, x_access_token)

    @classmethod
    async def authenticate(cls, uow: IUnitOfWork, access_token: str) -> UserDTO | None:
        if not access_token:
            return None
        async with uow:
            try:
                decoded_token = cls._validate_and_return_decoded(access_token)
            except jwt.exceptions.PyJWTError:
                raise http_exc.UnauthorizedHTTPException
            user = await uow.users.get_one_by_id(decoded_token["user_id"])
            await uow.commit()
        return user

    @classmethod
    def _build_tokens_pair(cls, user_id: int) -> TokensPairDTO:
        access_token_exp = int(
            (datetime.datetime.now(datetime.UTC) +
             datetime.timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        )
        refresh_token_exp = int(
            (datetime.datetime.now(datetime.UTC) +
             datetime.timedelta(minutes=jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES)).timestamp()
        )
        return TokensPairDTO(
            access_token=cls._jwt_encode(
                {
                    'user_id': user_id,
                    'type': 'access',
                }
            ),
            access_token_expires=access_token_exp,
            refresh_token=cls._jwt_encode(
                {
                    'user_id': user_id,
                    'type': 'refresh',
                }
            ),
            refresh_token_expires=refresh_token_exp,
        )

    @classmethod
    def _validate_and_return_decoded(cls, token: str) -> dict[str, Any] | None:
        decoded_token = cls._jwt_decode(token)
        user_id = decoded_token.get('user_id')
        if not user_id:
            return None
        if decoded_token.get('type') != 'access':
            return None
        return decoded_token

    @classmethod
    def _jwt_decode(cls, token: str) -> dict:
        return jwt.decode(
            token,
            jwt_settings.SECRET_KEY,
            algorithms=[jwt_settings.ALGORITHM],
            leeway=60,
        )

    @classmethod
    def _jwt_encode(cls, token: str) -> str:
        return jwt.encode(
            token,
            jwt_settings.SECRET_KEY,
            algorithm=jwt_settings.ALGORITHM,
        )
