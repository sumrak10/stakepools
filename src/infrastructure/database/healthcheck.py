import socket

from sqlalchemy import text

from src.infrastructure.database.base import engine
from src.utils.exceptions.healthchecks import DatabaseHealthCheckError


async def healthcheck() -> None:
    engine.echo = False
    try:
        async with engine.connect() as session:
            await session.execute(text("SELECT 1"))
    except socket.gaierror as e:
        raise DatabaseHealthCheckError from e
    except socket.timeout as e:
        raise DatabaseHealthCheckError from e
    except OSError as e:
        raise DatabaseHealthCheckError from e
    engine.echo = True
