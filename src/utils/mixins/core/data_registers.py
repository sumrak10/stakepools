from sqlalchemy import BOOLEAN
from sqlalchemy.orm import mapped_column

from models.utils.metadata import CoreBase


class DataRegisterMixin(CoreBase):
    __abstract__ = True


class DataRegisterDTOMixin:
    pass
