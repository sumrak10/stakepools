from sqlalchemy import BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped

from models.utils.metadata import CoreBase


class HandBookMixin(CoreBase):
    __abstract__ = True

    system__not_editable: Mapped[bool] = mapped_column(BOOLEAN, default=False)


class HandBookDTOMixin:
    system__not_editable: bool
