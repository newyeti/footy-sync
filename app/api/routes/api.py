from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.routes import health_check, teams


router = APIRouter()
router.include_router(router=health_check.router, tags=["admin"], prefix="")
router.include_router(router=teams.router, tags=["teams"], prefix="")
