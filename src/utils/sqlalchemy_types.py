from typing import Annotated, Optional
from decimal import Decimal

from sqlalchemy import Numeric, String, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column

CryptoAmount = Annotated[int, mapped_column(BigInteger())]
