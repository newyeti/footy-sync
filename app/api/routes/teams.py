from typing import Any

from fastapi import APIRouter, status

router = APIRouter()

@router.post("/teams/{season}/{league_id}", 
            name="teams:sync_teams",
            summary = "Synchornize teams data",
            description = "Retrive teams data from API and updates database",
            status_code=status.HTTP_200_OK)
async def sync_teams() -> Any:
    ...