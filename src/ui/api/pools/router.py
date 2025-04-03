from typing import Annotated

from fastapi import APIRouter, Depends, Body, Header
from starlette.websockets import WebSocket

from src.application.transport.pools.pools import PoolUserDTO, PoolDTO, PoolWithUserTXDTO
from src.application.transport.users.users import UserDTO
from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.auth.jwt import JWTAuthUseCase
from src.application.use_cases.pools.pools import PoolsUseCase
from src.infrastructure.blockchain.transactions_manager import TransactionsManager
from src.utils.api import responses
from src.utils.exceptions import http_exc

router = APIRouter()


@router.get(
    path="/pools",
    response_model=list[PoolWithUserTXDTO],
    responses={
        **http_exc.NotFoundHTTPException.docs(),
    },
)
async def get_my_pools(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    current_user: Annotated[UserDTO, Depends(JWTAuthUseCase.current_user)],
) -> None:
    uow.current_user = current_user
    return await PoolsUseCase.get_user_pools(uow)


@router.get(
    path="/pools/all",
    response_model=list[PoolDTO],
    responses={
        **http_exc.NotFoundHTTPException.docs(),
    },
)
async def get_all_pools(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    current_user: Annotated[UserDTO, Depends(JWTAuthUseCase.current_user)],
) -> None:
    uow.current_user = current_user
    return await PoolsUseCase.get_all_pools(uow)


@router.post(
    path="/pools",
    response_model=PoolDTO,
    responses={
        **http_exc.NotFoundHTTPException.docs(),
        **responses.ObjectCreatedResponse.docs(),
    },
)
async def deposit_to_pool(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    current_user: Annotated[UserDTO, Depends(JWTAuthUseCase.current_user)],
    pool_id: int = Body(...),
    amount: int = Body(...),
) -> None:
    uow.current_user = current_user
    pool_user_id = await PoolsUseCase.deposit_to_pool(uow, pool_id, amount)
    return responses.ObjectCreatedResponse.response(_detail={"id": pool_user_id})


@router.websocket(
    path="/pools/ws",
)
async def websocket_endpoint(
    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
    websocket: WebSocket,
    x_access_token: str = Header(...),
):
    async with uow:
        uow.current_user = await JWTAuthUseCase.authenticate(uow, x_access_token)
        await uow.commit()
    await websocket.accept()
    await TransactionsManager().link_websocket_client(uow.current_user.id, websocket)
    while True:
        data = await websocket.receive_json()
        if data["action"] == "ping":
            await websocket.send_text(f"Pong")
