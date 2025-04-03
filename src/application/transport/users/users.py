from pydantic import BaseModel
from pydantic import SecretStr


class UserDTO(BaseModel):
    id: int
    email: str
    password: SecretStr
    is_active: bool
    is_verified: bool


class UserCreateDTO(BaseModel):
    email: str
    password: SecretStr


class UserLoginDTO(BaseModel):
    email: str
    password: SecretStr

