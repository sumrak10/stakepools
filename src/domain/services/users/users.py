from src.application.transport.users.users import UserDTO, UserCreateDTO
from src.application.uow.uow import IUnitOfWork
from src.utils.passwords import PasswordsService


class UsersService:
    @classmethod
    async def get_by_id(cls, uow: IUnitOfWork) -> UserDTO | None:
        """Get user by id."""
        return await uow.users.get_one_by_id(uow.current_user.id)

    @classmethod
    async def register(cls, uow: IUnitOfWork, create_dto: UserCreateDTO) -> int:
        """Register a new user.
        :raises:
        """
        # TODO: Implement email verification and uniqueness check
        # if await uow.users.get_one_by_email(create_dto.email) is not None:
        #     raise ValueError("User with this email already exists")
        if create_dto.password is not None:
            create_dto.password = PasswordsService.get_password_hash(
                create_dto.password.get_secret_value()
            )
        return await uow.users.create_one(create_dto)
