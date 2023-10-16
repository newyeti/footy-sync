from fastapi import APIRouter

from app.api.routes import health_check

router = APIRouter()
router.include_router(router=health_check.router, tags=["admin"], prefix="")