from __future__ import annotations

import json
import logging
from typing import NoReturn, Annotated
from typing import TYPE_CHECKING

from fastapi import Header, Depends

from src.application.transport.users.users import UserDTO

from src.config.server import server_settings
from src.infrastructure.database.base import async_session_maker
from src.infrastructure.repositories.sqlalchemy_orm.pools.pools import PoolsRepository
from src.infrastructure.repositories.sqlalchemy_orm.users.users import UsersRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class IUnitOfWork:
    users: UsersRepository
    pools: PoolsRepository

    def init_repositories(self, session: AsyncSession) -> None:
        self.users = UsersRepository(session)
        self.pools = PoolsRepository(session)

    def __init__(
        self,
        x_accept_language: str = Header(default='ru', example='ru'),
    ) -> None:
        self.logger = logging.getLogger(__name__)

        self.session_factory = async_session_maker
        self._session = None
        self._session_nesting_level = 0

        self._current_language: str | None = x_accept_language
        self._current_user: UserDTO = None

    @property
    def current_user(self) -> UserDTO | None:
        return self._current_user

    @current_user.setter
    def current_user(self, user: UserDTO) -> None:
        self._current_user = user

    @property
    def current_language(self) -> str | None:
        return self._current_language or server_settings.DEFAULT_LANGUAGE

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                'An attempt to access the session was unsuccessful. Maybe you forgot to initialize it '
                'via __aenter__ (async with uow)',
            )
        return self._session

    async def __aenter__(self) -> None:
        """Call when entering the context manager."""
        self._session_nesting_level += 1
        if self._session_nesting_level == 1:  # if session is not initialized
            self._session = self.session_factory()
            self.init_repositories(self._session)

    async def __aexit__(self, *args: object) -> None:
        """Call when exiting the context manager."""
        if self._session_nesting_level == 1 and self._session is not None:  # if session is initialized
            await self.rollback()
        self._session_nesting_level -= 1

    async def commit(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.commit()
            await self.session.close()
            self._session = None

    async def rollback(self) -> None:
        if self._session_nesting_level == 1:
            await self.session.rollback()
            await self.session.close()
            self._session = None

    def __getattr__(self, item: str) -> NoReturn:
        """Call when the attribute is not found in the object."""
        raise AttributeError(
            f'Attribute {item} not found. If you want to access the repository, '
            f'you need to initialize it via __aenter__ (async with uow)',
        )
