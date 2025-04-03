from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.utils.metadata import Base


class TimestampMixin(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )


class TimestampDTOMixin:
    created_at: datetime
    updated_at: datetime | None
