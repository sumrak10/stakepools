from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, select, func
from sqlalchemy.orm import Mapped, relationship, column_property
from sqlalchemy.orm import mapped_column

from src.application.transport.pools.pools import PoolUserDTO, PoolDTO, PoolStatus
from src.utils.metadata import Base
from src.utils.mixins.common import TimestampMixin
from src.utils.sqlalchemy_types import CryptoAmount
from src.domain.models.transactions.transactions import TransactionModel

if TYPE_CHECKING:
    from src.domain.models.users.users import UserModel


class PoolUserModel(TimestampMixin, Base):
    __tablename__ = 'pools__users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pool_id: Mapped[int] = mapped_column(ForeignKey('pools.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    transaction_id: Mapped[int | None] = mapped_column(ForeignKey('transactions.id'))
    deposit_amount: Mapped[CryptoAmount]

    pool: Mapped['PoolModel'] = relationship(backref='pool_users', lazy='noload')
    user: Mapped['UserModel'] = relationship(backref='pools', lazy='noload')
    transaction: Mapped['TransactionModel'] = relationship(backref='pool_users', lazy='noload')

    def to_dto(self) -> PoolUserDTO:
        return PoolUserDTO(
            id=self.id,
            pool_id=self.pool_id,
            user_id=self.user_id,
            deposit_amount=self.deposit_amount,
            pool=self.pool.to_dto() if self.pool else None,
            user=self.user.to_dto() if self.user else None,
        )


class PoolModel(TimestampMixin, Base):
    __tablename__ = 'pools'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    promised_percentage: Mapped[int]
    execution_days: Mapped[int]
    expected_amount: Mapped[CryptoAmount]
    status: Mapped[PoolStatus] = mapped_column(default=PoolStatus.DRAFT)

    current_amount: Mapped[CryptoAmount] = column_property(
        select(
            func.sum(TransactionModel.amount)
        )
        .join(
            PoolUserModel,
            PoolUserModel.transaction_id == TransactionModel.id
        )
        .where(
            PoolUserModel.pool_id == id
        )
        .group_by(
            PoolUserModel.pool_id
        )
        .scalar_subquery()
    )

    def to_dto(self) -> PoolDTO:
        return PoolDTO(
            id=self.id,
            promised_percentage=self.promised_percentage,
            execution_days=self.execution_days,
            expected_amount=self.expected_amount,
            status=self.status,
            current_amount=self.current_amount if self.current_amount else 0,
        )
