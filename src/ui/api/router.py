from fastapi import APIRouter

from src.utils.exceptions import http_exc

from .auth import router as auth_router
from .users import router as users_router
from .pools import router as pools_router

router = APIRouter(
    prefix="/api/v1",
    responses={
        **http_exc.UnauthorizedHTTPException.docs(),
        **http_exc.ForbiddenHTTPException.docs(),
    }
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(pools_router)
