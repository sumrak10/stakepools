from typing import TYPE_CHECKING

from src.infrastructure.repositories.abstract_repository import AbstractRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AbstractSQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: 'AsyncSession') -> None:
        super().__init__(session)
