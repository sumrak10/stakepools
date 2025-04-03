from sqlalchemy import insert, select

from src.application.transport.transactions.transactions import TransactionDTO
from src.domain.models.transactions.transactions import TransactionModel
from src.infrastructure.repositories.sqlalchemy_orm.abstract_repository import AbstractSQLAlchemyRepository


class TransactionsRepository(AbstractSQLAlchemyRepository):
    async def create_one(self, create_dto: TransactionDTO) -> int:
        stmt = (
            insert(
                TransactionModel
            )
            .values(
                **create_dto.model_dump(),
            )
            .returning(
                TransactionModel.id
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_id_by_hash(self, tx_id: str) -> int | None:
        stmt = (
            select(
                TransactionModel.id
            )
            .where(
                TransactionModel.tx_id == tx_id,
            )
        )
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

