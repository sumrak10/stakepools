from fastapi import APIRouter

from .router import router as api_router


router = APIRouter()

router.include_router(api_router)
