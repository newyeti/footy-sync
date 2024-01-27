from fastapi import APIRouter, Depends
from app.api.routes import (
    admin, 
    teams, 
    fixtures, 
    standings, 
    top_scorers
)

router = APIRouter()
router.include_router(router=admin.router, tags=["admin"], prefix="")
router.include_router(router=teams.router, tags=["teams"], prefix="")
router.include_router(router=fixtures.router, tags=["fixtures"], prefix="")
router.include_router(router=standings.router,tags=["staindings"], prefix="")
router.include_router(router=top_scorers.router, tags=["top_scorers"], prefix="")