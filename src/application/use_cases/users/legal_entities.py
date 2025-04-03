from fastapi import BackgroundTasks
from models.dto.users.legal_entity import LegalEntityInputDTO, LegalEntityCreateDTO
from models.dto.users.users import UserInputDTO
from models.utils.choices.users import UserType
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.application.transport.users.requests import LegalEntityCreateRequestDTO
from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.auth.eds import EDSAuthUseCase
from src.application.use_cases.databases.databases import DatabasesUseCase
from src.domain.services.auth.session_tokens import SessionAuthService
from src.domain.services.users.users import UsersService
from src.utils.api import responses
from src.utils.exceptions import http_exc


class LegalEntityUsersUseCase:
    @classmethod
    async def register(cls,
                       request: Request,
                       uow: IUnitOfWork,
                       bg_tasks: BackgroundTasks,
                       real_ip: str,
                       forwarded_for: str,
                       request_dto: LegalEntityCreateRequestDTO,
                       legal_entity_input_dto: LegalEntityInputDTO,
                       ) -> JSONResponse:
        """Register a new user
        :param cls:
        :param request:
        :param uow:
        :param bg_tasks:
        :param real_ip:
        :param forwarded_for:
        :param request_dto:
        :param legal_entity_input_dto:
        :return:
        :raises: InvalidOTPCodeHTTPException.
        """
        if request_dto.type != UserType.JURIDICAL:
            raise http_exc.BadRequestHTTPException("User type must be juridical")
        if request_dto.password is not None:
            raise http_exc.BadRequestHTTPException("Password must be None")

        subject_certificate_info = await EDSAuthUseCase.auth(real_ip, forwarded_for, request_dto.eds)
        subject_name_inn, _ = EDSAuthUseCase.pull_subject_inn_pinfl(
            subject_certificate_info.subject_name
        )
        if subject_name_inn is None:
            raise http_exc.UnauthorizedHTTPException("User is not juridic type")
        subject_name_name = subject_certificate_info.subject_name.get('CN')

        async with uow:
            try:
                user_id = await UsersService.register(
                    uow,
                    UserInputDTO(**request_dto.model_dump())
                )
            except ValueError as e:
                raise http_exc.BadRequestHTTPException(str(e))

            await uow.users.create_legal_entity(
                LegalEntityCreateDTO(
                    user_id=user_id,
                    inn=subject_name_inn,
                    name=subject_name_name,
                    **legal_entity_input_dto.model_dump()
                )
            )
            name = subject_name_name
            bank = None
            address = None
            mfo = None
            phone = None
            inn = subject_name_inn
            account = None

            await DatabasesUseCase.create(
                uow,
                bg_tasks,
                name,
                bank,
                address,
                mfo,
                phone,
                inn,
                account,
            )

            response = responses.ObjectCreatedResponse.response(_detail={"id": user_id})
            await SessionAuthService.on_login_event(
                uow,
                request,
                response,
                user_id,
            )
            await uow.commit()
        return response
