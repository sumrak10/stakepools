from enum import Enum
from typing import Optional

from pydantic import BaseModel

from src.application.transport.transactions.transactions import TransactionInDBDTO
from src.application.transport.users.users import UserDTO


class PoolStatus(str, Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class PoolDTO(BaseModel):
    id: int
    promised_percentage: int
    execution_days: int
    expected_amount: int
    current_amount: int | None = None
    status: PoolStatus


class PoolUserDTO(BaseModel):
    id: int
    pool_id: int
    user_id: int
    deposit_amount: int

    pool: Optional['PoolDTO'] = None
    user: Optional['UserDTO'] = None


PoolUserDTO.model_rebuild()


class PoolWithUserTXDTO(PoolDTO):
    deposit_amount_summ: int
    deposit_transactions: list[TransactionInDBDTO]
