import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.infrastructure.blockchain.transactions_manager import TransactionsManager
from src.infrastructure.blockchain.trongrid.trongrid_pooling import TrongridPooling
from src.ui.api.router import router as api_router
from src.utils.metadata import Base


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    # Database init
    from src.infrastructure.database.base import engine
    from src.infrastructure.database.healthcheck import healthcheck as db_healthcheck
    await db_healthcheck()  # Check database connection
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Trongrid pooling init
    transactions_queue = asyncio.Queue()
    trongrid_pooling = TrongridPooling(transactions_queue)
    asyncio.create_task(trongrid_pooling.start_long_pooling())
    transaction_manager = TransactionsManager()
    transaction_manager.set_queue(transactions_queue)
    asyncio.create_task(transaction_manager.process_transcations())

    try:
        yield
    finally:
        # Trongrid pooling shutdown
        await trongrid_pooling.shutdown()
        # Transactions manager shutdown
        await transaction_manager.shutdown()

        # Database shutdown
        await engine.dispose()  # Clean up the connection pool


def create_app() -> FastAPI:
    app_ = FastAPI(
        title='Core Service',
        version='1.0.0',
        lifespan=lifespan,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=[],
    )

    @app_.get('/metrics')
    async def metrics() -> JSONResponse:
        return JSONResponse({'message': 'ok'}, status_code=status.HTTP_200_OK)

    app_.include_router(api_router)

    return app_
