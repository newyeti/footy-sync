from fastapi import APIRouter, Depends
from app.api.routes import admin, teams, fixtures

router = APIRouter()
router.include_router(router=admin.router, tags=["admin"], prefix="")
router.include_router(router=teams.router, tags=["teams"], prefix="")
router.include_router(router=fixtures.router, tags=["fixtures"], prefix="")
