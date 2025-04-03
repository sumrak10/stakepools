import asyncio
import dataclasses
import logging

import asyncpg
import sqlalchemy
from fastapi.websockets import WebSocket

from src.application.transport.pools.pools import PoolUserDTO
from src.application.transport.transactions.transactions import TransactionDTO
from src.infrastructure.database.base import async_session_maker
from src.infrastructure.repositories.sqlalchemy_orm.pools.pools import PoolsRepository
from src.infrastructure.repositories.sqlalchemy_orm.transactions.transactions import TransactionsRepository
from src.utils.singleton import Singleton


class TransactionsManager(metaclass=Singleton):
    def __init__(self):
        self._queue = None
        self._shutdown_event = asyncio.Event()
        self.ws_list: dict[int, WebSocket] = {}

    def set_queue(self, queue: asyncio.Queue):
        self._queue = queue

    async def shutdown(self):
        self._shutdown_event.set()

    async def process_transcations(self):
        while not self._shutdown_event.is_set():
            raw_transaction = await self._queue.get()
            logging.info(f"Processing transaction: {raw_transaction}")
            transaction = TransactionDTO.from_raw(raw_transaction)

            async with async_session_maker() as session:
                transactions_repo = TransactionsRepository(session)
                transaction_id = await transactions_repo.get_id_by_hash(transaction.tx_id)
                if transaction_id is not None:
                    continue

                transaction_id = await transactions_repo.create_one(transaction)
                logging.warning(f"Transaction with hash {transaction.tx_id} created")

                pools_repo = PoolsRepository(session)
                pool_user = await pools_repo.get_pool_user_id_by_amount(transaction.amount)
                if pool_user is not None:
                    await pools_repo.link_transaction_to_deposit(pool_user.id, transaction_id)
                    await self.notify_websocket_client(pool_user.user_id, pool_user)

                await session.commit()

    async def notify_websocket_client(self, user_id: int, pool_user: PoolUserDTO):
        logging.info(f"Sending new deposit with amount={pool_user.deposit_amount} notification to user: {user_id}")
        ws = self.ws_list.get(user_id)
        if ws is not None:
            await ws.send_json({
                'event': 'new_deposit',
                'data': pool_user.model_dump(),
            })
        else:
            logging.warning(f"Websocket client for user {user_id} not found")

    async def link_websocket_client(
            self,
            user_id: int,
            ws: WebSocket,
    ):
        self.ws_list[user_id] = ws
