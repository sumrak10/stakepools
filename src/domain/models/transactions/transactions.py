from typing import Any

from sqlalchemy import BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.application.transport.transactions.transactions import TransactionInDBDTO
from src.utils.metadata import Base
from src.utils.mixins.common import TimestampMixin
from src.utils.sqlalchemy_types import CryptoAmount


class TransactionModel(TimestampMixin, Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tx_id: Mapped[str] = mapped_column(index=True, unique=True)
    contract_address: Mapped[str | None] = mapped_column(index=True)
    amount: Mapped[CryptoAmount]
    from_address: Mapped[str] = mapped_column(index=True)
    to_address: Mapped[str] = mapped_column(index=True)
    timestamp: Mapped[int] = mapped_column(BigInteger())

    raw_transaction: Mapped[dict[str, Any]] = mapped_column(JSONB())

    def to_dto(self) -> TransactionInDBDTO:
        return TransactionInDBDTO.model_validate(self, from_attributes=True)
