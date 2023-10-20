from typing import Any

from fastapi import APIRouter, status

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def health() -> Any:
    return {"status": "Running"}