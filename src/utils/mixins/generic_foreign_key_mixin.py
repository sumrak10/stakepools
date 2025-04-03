from sqlalchemy import Enum, inspect
from sqlalchemy.orm import Mapped, mapped_column

from models.utils.choices.core.documents.documents import DocumentTypeEnum
from models.utils.metadata import CoreBase


class GenericForeignKeyMixin:
    """
    Mixin for implementing Generic Foreign Key using ORM.
    """

    document_type: Mapped[DocumentTypeEnum] = mapped_column(
        Enum(DocumentTypeEnum), nullable=True
    )
    document_id: Mapped[int] = mapped_column(nullable=True)

    @staticmethod
    def _get_model_by_tablename(tablename: str):
        """
        Находит модель по названию таблицы.
        """
        for class_ in CoreBase.registry.mappers:
            model = class_.class_
            if inspect(model).local_table.name == tablename:
                return model
        raise ValueError(f"Модель с __tablename__='{tablename}' не найдена.")
