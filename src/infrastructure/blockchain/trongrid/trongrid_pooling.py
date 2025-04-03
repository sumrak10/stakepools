import asyncio
import datetime
import logging
from typing import Any

import aiohttp

from src.config.blockchain import blockchain_settings
from src.config.trongrid import trongrid_settings
from src.utils.singleton import Singleton


class TrongridPooling(metaclass=Singleton):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self._last_update_timestamp = 0
        self._shutdown_event = asyncio.Event()
        self._session = aiohttp.ClientSession(trongrid_settings.BASE_URL)

    async def shutdown(self):
        self._shutdown_event.set()
        await self._session.close()

    async def start_long_pooling(self):
        logging.info("Trongrid.LongPooling: Starting")
        fingerprint = None
        last_update_timestamp = self._last_update_timestamp
        while not self._shutdown_event.is_set():
            transactions, fingerprint = await self._fetch_transactions(fingerprint)
            for transaction in transactions:
                logging.debug("Trongrid.LongPooling: Transaction putted into queue: ", transaction["transaction_id"])
                await self.queue.put(transaction)
                if last_update_timestamp < transaction["block_timestamp"]:
                    last_update_timestamp = transaction["block_timestamp"]
            if fingerprint is not None:
                continue  # If fingerprint is not None, we need to fetch more transactions

            if last_update_timestamp is not None:
                self._last_update_timestamp = last_update_timestamp
            logging.info("Trongrid.LongPooling: Received %s transactions", len(transactions))
            await asyncio.sleep(60 / trongrid_settings.LONG_POOLING_RPM_FREQ)
        logging.info("Trongrid.LongPooling: Stopped")

    async def _fetch_transactions(self, fingerprint: str) -> tuple[dict[str, Any], str | None]:
        params = {
            "only_to": "true",
            "only_confirmed": "true",
            "min_timestamp": self._last_update_timestamp,
            "limit": 200,
            "order_by": "block_timestamp,desc",
        }
        if fingerprint:
            params["fingerprint"] = fingerprint
        logging.info(f"Trongrid.LongPooling: Sending req with params: {params}. Fingerprint: {fingerprint}", )
        async with self._session.get(
            f"v1/accounts/{blockchain_settings.TRC20_ADDRESS}/transactions/trc20",
            params=params
        ) as response:
            if response.status != 200:
                raise Exception(await response.text())
            json = await response.json()
        data = []
        for transaction in json["data"]:
            if transaction["block_timestamp"] <= self._last_update_timestamp:
                continue
            data.append(transaction)
        return data, json["meta"].get(fingerprint)


