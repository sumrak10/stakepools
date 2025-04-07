from src.application.transport.pools.pools import PoolUserDTO, PoolDTO, PoolWithUserTXDTO
from src.application.uow.uow import IUnitOfWork
from src.utils.blockchain import generate_memo


class PoolsUseCase:
    @classmethod
    async def get_user_pools(cls, uow: IUnitOfWork) -> list[PoolWithUserTXDTO]:
        async with uow:
            pools = await uow.pools.get_user_pools(uow.current_user.id, is_revenue=False)
            revenue_pools = await uow.pools.get_user_pools(uow.current_user.id, is_revenue=True)
            for pool in pools:
                for revenue_pool in revenue_pools:
                    if pool.id == revenue_pool.id:
                        pool.revenue_amount = revenue_pool.deposit_amount_summ
                        pool.revenue_transactions = revenue_pool.deposit_transactions
            await uow.commit()
        return pools

    @classmethod
    async def get_all_pools(cls, uow: IUnitOfWork) -> list[PoolDTO]:
        async with uow:
            pools = await uow.pools.get_all()
            await uow.commit()
        return pools

    @classmethod
    async def deposit_to_pool(cls, uow: IUnitOfWork, pool_id: int, amount: int) -> int:
        async with uow:
            pool_user_id = await uow.pools.create_deposit(pool_id, uow.current_user.id, amount, None)
            await uow.commit()
        return pool_user_id
