from src.application.transport.users.users import UserCreateDTO, UserDTO
from src.application.uow.uow import IUnitOfWork
from src.domain.services.users.users import UsersService
from src.utils.choices.otp_type import OTPType
from src.utils.exceptions import http_exc
from src.utils.passwords import PasswordsService


class UsersUseCase:
    @classmethod
    async def register(cls,
                       uow: IUnitOfWork,
                       create_dto: UserCreateDTO,
                       ) -> int:
        """Register a new user
        :param cls:
        :param uow:
        :param create_dto:
        :return:
        :raises: InvalidOTPCodeHTTPException.
        """
        async with uow:
            try:
                user_id = await UsersService.register(
                    uow,
                    create_dto
                )
            except ValueError as e:
                raise http_exc.BadRequestHTTPException(str(e))
            await uow.commit()
        return user_id

    @classmethod
    async def get_user_by_id(cls,
                             uow: IUnitOfWork,
                             ) -> UserDTO:
        """Get user by id
        :param cls:
        :param uow:
        :return:
        :raises: NotFoundHTTPException, ForbiddenHTTPException, UnauthorizedHTTPException.
        """
        async with uow:
            user = await UsersService.get_by_id(uow)
            if user is None:
                msg = "User not found"
                raise http_exc.NotFoundHTTPException(msg)
            await uow.commit()
        return user
