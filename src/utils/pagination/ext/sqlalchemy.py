import logging
from typing import TypeVar, Callable

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from models.dto.pagination.page import Page
from models.utils.exceptions.database_error import DatabaseException

logger = logging.getLogger(__name__)
T = TypeVar('T', bound=BaseModel)


async def paginate(
    session: AsyncSession,
    base_stmt: Select,
    *,
    page_size_dto: BaseModel,
    count_stmt: Select | None = None,
    unique: bool = False,
    to_dto_func: Callable = None,
) -> Page[T]:
    try:
        count_res = await session.execute(
            count_stmt if count_stmt is not None else select(func.count()).select_from(base_stmt.subquery()),
        )
    except ProgrammingError as e:
        logger.error(e)
        raise DatabaseException(str(e))
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseException(str(e))
    except Exception as e:
        logger.error(e)
        raise DatabaseException(str(e))

    total = count_res.scalar_one()

    limit_offset_stmt = base_stmt.limit(page_size_dto.size).offset((page_size_dto.page - 1) * page_size_dto.size)

    try:
        res = await session.execute(limit_offset_stmt)
    except ProgrammingError as e:
        logger.error(e)
        raise DatabaseException(str(e))
    except DatabaseError as e:
        logger.error(e)
        raise DatabaseException(str(e))
    except Exception as e:
        logger.error(e)
        raise DatabaseException(str(e))

    # Unique results
    if unique:
        res = res.unique()

    # Validating results
    if res is not None:
        if to_dto_func is not None:
            res = [to_dto_func(row) for row in res.all()]
        else:
            res = [row.to_dto() for row in res.scalars().all()]

    return Page(
        page=page_size_dto.page,
        size=page_size_dto.size,
        count=total,
        items=res,
    )
