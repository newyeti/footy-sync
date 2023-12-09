from fastapi import APIRouter, Depends
from app.api.routes import admin, teams

router = APIRouter()
router.include_router(router=admin.router, tags=["admin"], prefix="")
router.include_router(router=teams.router, tags=["teams"], prefix="")
