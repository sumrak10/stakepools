from passlib.context import CryptContext
from pydantic import SecretStr


class PasswordsService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls: type["PasswordsService"],
                        raw_password: str,
                        hashed_password: str) -> bool:
        return cls.pwd_context.verify(raw_password, hashed_password)

    @classmethod
    def get_password_hash(cls: type["PasswordsService"], password: str) -> SecretStr:
        return SecretStr(cls.pwd_context.hash(password))
