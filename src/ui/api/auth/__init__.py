from fastapi import APIRouter

from .router import router as main_router


router = APIRouter(
    prefix="/auth",
)


router.include_router(main_router)
