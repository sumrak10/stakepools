from models.dto.users.users import UserInputDTO
from models.utils.choices.otp_type import OTPType
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.transport.users.requests import IndividualCreateRequestDTO
from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.users.users import UsersUseCase
from src.domain.services.auth.session_tokens import SessionAuthService
from src.domain.services.otp.otp import OTPService
from src.utils.api import responses
from src.utils.exceptions import http_exc


class IndividualUsersUseCase:
    @classmethod
    async def register(cls,
                       request: Request,
                       uow: IUnitOfWork,
                       request_dto: IndividualCreateRequestDTO,
                       ) -> JSONResponse:
        """Register a new user
        :param cls:
        :param request:
        :param uow:
        :param request_dto:
        :return:
        :raises: InvalidOTPCodeHTTPException.
        """
        async with uow:
            if not await OTPService.is_verified(uow, request_dto.phone, OTPType.REGISTRATION, request_dto.otp_code):
                raise http_exc.InvalidOTPCodeHTTPException("Invalid OTP code. Please try to create OTP code.")

            if await uow.users.get_one_by_phone(request_dto.phone) is not None:
                raise ValueError("User with this phone already exists")
            user_id = await UsersUseCase.register(uow, UserInputDTO(**request_dto.model_dump()))
            response = responses.ObjectCreatedResponse.response(_detail={"id": user_id})
            await SessionAuthService.on_login_event(
                uow,
                request,
                response,
                user_id,
            )
            await uow.commit()
        return user_id
