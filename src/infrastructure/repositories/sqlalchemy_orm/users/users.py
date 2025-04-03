from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import insert, update, select, func

from src.application.transport.users.users import UserCreateDTO, UserDTO
from src.domain.models.users.users import UserModel
from src.infrastructure.repositories.sqlalchemy_orm.abstract_repository import AbstractSQLAlchemyRepository


class UsersRepository(AbstractSQLAlchemyRepository):
    async def create_one(self, account: UserCreateDTO) -> int:
        data = account.model_dump(exclude='password')
        if account.password is not None:
            data["password"] = account.password.get_secret_value()
        else:
            data["password"] = None
        stmt = (
            insert(UserModel)
            .values(
                **data,
            )
            .returning(UserModel.id)
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    # async def update_one(self, account_id: int, account: UserUpdateDTO) -> None:
    #     data = account.model_dump(exclude_none=True)
    #     stmt = (
    #         update(UserModel)
    #         .where(UserModel.id == account_id)
    #         .values(
    #             **data,
    #         )
    #     )
    #     await self._session.execute(stmt)

    # async def update_password(self, account_id: int, password: str) -> None:
    #     stmt = (
    #         update(UserModel)
    #         .where(UserModel.id == account_id)
    #         .values(
    #             password=password,
    #         )
    #     )
    #     await self._session.execute(stmt)

    async def get_one_by_id(self, account_id: int) -> Optional['UserDTO']:
        stmt = select(UserModel).where(UserModel.id == account_id)
        res = await self._session.execute(stmt)
        row = res.scalar_one_or_none()
        return UserDTO.model_validate(row, from_attributes=True) if row is not None else None

    async def get_one_by_email(self, email: str) -> Optional['UserDTO']:
        stmt = select(UserModel).where(UserModel.email == email)
        res = await self._session.execute(stmt)
        row = res.scalar_one_or_none()
        return UserDTO.model_validate(row, from_attributes=True) if row is not None else None
