from sqlalchemy import BOOLEAN, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from models.utils.metadata import CoreBase


class CoreBaseMixin(CoreBase):
    __abstract__ = True

    system__deleted: Mapped[bool] = mapped_column(BOOLEAN, default=False)


class CoreBaseDTOMixin:
    system__deleted: bool
