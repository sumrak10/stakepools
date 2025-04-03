import datetime
import hashlib

from sqlalchemy import String, Index, func, Constraint
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from models.utils.choices.core.documents.statuses import DocumentStatusEnum
from models.utils.metadata import CoreBase


class DocumentMixin(CoreBase):
    __abstract__ = True

    code: Mapped[str | None] = mapped_column(String(12), nullable=True)
    date: Mapped[datetime.date]
    mark__as_archived: Mapped[bool] = mapped_column(default=False)
    mark__for_deletion: Mapped[bool] = mapped_column(default=False)
    system__status: Mapped[DocumentStatusEnum] = mapped_column(
        default=DocumentStatusEnum.DRAFT
    )

    @classmethod
    @declared_attr
    def __table_args__(cls):
        # Сокращаем имя таблицы и добавляем хэш для уникальности индекса
        idx_name = f"{cls.__tablename__[:20]}_{hashlib.md5(cls.__tablename__.encode()).hexdigest()[:8]}__code_year_idx"

        # Создаем индекс с выражением для year
        mixin_index = Index(
            idx_name,
            "code",
            func.date_part("year", cls.date),  # Используем явное обращение к столбцу
            unique=True,
        )

        # Получаем существующие __table_args__, если они есть
        parent_table_args = getattr(cls, "__orig_table_args__", ())

        if isinstance(parent_table_args, dict):
            # Если это словарь, возвращаем индекс и словарь
            return (mixin_index,), parent_table_args
        elif isinstance(parent_table_args, tuple):
            # Если это кортеж, добавляем индекс к нему
            return mixin_index, *parent_table_args
        else:
            # Если ничего не задано, возвращаем только индекс
            return (mixin_index,)


class DocumentDTOBaseMixin:
    code: str | None = None
    data: str | None = None


class DocumentDTOSystemMixin(DocumentDTOBaseMixin):
    mark__as_archived: bool
    mark__for_deletion: bool
    system__status: DocumentStatusEnum
