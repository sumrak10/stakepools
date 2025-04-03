from typing import Any

from pydantic import BaseModel

from src.utils.blockchain import hex_to_base58, USDT_CONTRACT_ADDRESS


class TransactionDTO(BaseModel):
    tx_id: str
    contract_address: str | None
    amount: int
    from_address: str
    to_address: str
    timestamp: int

    raw_transaction: dict[str, Any] | None = None

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> 'TransactionDTO':
        return TransactionDTO(
            tx_id=raw["transaction_id"],
            contract_address=raw["token_info"]["address"],
            amount=raw["value"],
            from_address=raw["from"],
            to_address=raw["to"],
            timestamp=raw["block_timestamp"],
            raw_transaction=raw,
        )

    def is_usdt(self) -> bool:
        return self.contract_address == USDT_CONTRACT_ADDRESS


class TransactionInDBDTO(TransactionDTO):
    id: int
