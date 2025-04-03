from sqlalchemy import Enum, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.application.transport.users.users import UserDTO
from src.utils.metadata import Base
from src.utils.mixins.common import TimestampMixin


class UserModel(TimestampMixin, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    def to_dto(self) -> UserDTO:
        return UserDTO.model_validate(self, from_attributes=True)

