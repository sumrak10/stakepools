from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
