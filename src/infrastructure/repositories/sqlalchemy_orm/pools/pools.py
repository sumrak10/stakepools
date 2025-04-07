

from typing import Any

from sqlalchemy import insert, select, update, func, and_, or_
from sqlalchemy.orm import joinedload, aliased

from src.application.transport.pools.pools import PoolDTO, PoolUserDTO, PoolStatus, PoolWithUserTXDTO
from src.domain.models import TransactionModel
from src.domain.models.pools.pools import PoolModel, PoolUserModel
from src.infrastructure.repositories.sqlalchemy_orm.abstract_repository import AbstractSQLAlchemyRepository


class PoolsRepository(AbstractSQLAlchemyRepository):
    async def create_deposit(self, pool_id: int, user_id: int, deposit_amount: int, transaction_id: str | None) -> int:
        stmt = (
            insert(
                PoolUserModel
            )
            .values(
                pool_id=pool_id,
                user_id=user_id,
                deposit_amount=deposit_amount,
                transaction_id=transaction_id,
            )
            .returning(
                PoolUserModel.id
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def link_transaction_to_deposit(self, pool_user_id: int, transaction_id: int) -> None:
        stmt = (
            update(
                PoolUserModel
            )
            .values(
                transaction_id=transaction_id,
            )
            .where(
                PoolUserModel.id == pool_user_id,
                PoolUserModel.transaction_id.is_(None),
            )
        )
        await self._session.execute(stmt)

    async def get_pool_user_id_by_amount(self, amount: int) -> PoolUserDTO:
        stmt = (
            select(
                PoolUserModel
            )
            .where(
                PoolUserModel.deposit_amount == amount
            )
        )
        res = await self._session.execute(stmt)
        res = res.scalars().first()
        if res is None:
            return None
        return res.to_dto()

    async def get_all(self) -> list[PoolDTO]:
        stmt = (
            select(
                PoolModel
            )
            .where(
                PoolModel.status == PoolStatus.ACTIVE
            )
        )
        res = await self._session.execute(stmt)
        return [pool.to_dto() for pool in res.scalars().all()]

    async def get_user_pools(self, user_id: int, is_revenue: bool) -> list[PoolWithUserTXDTO]:
        stmt = (
            select(
                PoolModel.id,
                PoolModel.promised_percentage,
                PoolModel.execution_days,
                PoolModel.expected_amount,
                PoolModel.status,
                PoolModel.created_at,
                func.sum(
                    PoolUserModel.deposit_amount
                ).label("amount_summ"),
                func.jsonb_agg(
                    func.jsonb_build_object(
                        "id", TransactionModel.id,
                        "tx_id", TransactionModel.tx_id,
                        "contract_address", TransactionModel.contract_address,
                        "amount", TransactionModel.amount,
                        "from_address", TransactionModel.from_address,
                        "to_address", TransactionModel.to_address,
                        "timestamp", TransactionModel.timestamp,
                    )
                ).label("deposit_transactions"),
            ).select_from(PoolModel)
            .join(PoolUserModel, and_(
                PoolUserModel.pool_id == PoolModel.id,
                PoolUserModel.user_id == user_id,
                PoolUserModel.transaction_id.is_not(None),
                PoolUserModel.is_revenue == is_revenue,
            ))
            .join(
                TransactionModel,
                TransactionModel.id == PoolUserModel.transaction_id,
            )
            .group_by(
                PoolModel.id,
                PoolModel.promised_percentage,
                PoolModel.execution_days,
                PoolModel.expected_amount,
                PoolModel.status,
                PoolModel.created_at,
            )
        )
        res = await self._session.execute(stmt)

        def to_dto(row):
            return PoolWithUserTXDTO(
                id=row["id"],
                promised_percentage=row["promised_percentage"],
                execution_days=row["execution_days"],
                expected_amount=row["expected_amount"],
                status=row["status"],
                created_at=row["created_at"],
                deposit_amount_summ=row["amount_summ"],
                revenue_amount=0,
                deposit_transactions=row["deposit_transactions"],
                revenue_transactions=[]
            )

        return [to_dto(row) for row in res.mappings().all()]
