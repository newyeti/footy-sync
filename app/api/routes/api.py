from fastapi import APIRouter, Depends
from app.api.routes import (
    admin, 
    teams, 
    fixtures, 
    standings, 
    top_statistics
)

router = APIRouter()
router.include_router(router=admin.router, tags=["admin"], prefix="")
router.include_router(router=teams.router, tags=["teams"], prefix="")
router.include_router(router=fixtures.router, tags=["fixtures"], prefix="")
router.include_router(router=standings.router,tags=["staindings"], prefix="")
router.include_router(router=top_statistics.router, tags=["players"], prefix="")