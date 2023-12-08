from typing import Any

from fastapi import APIRouter, status, Security
from app.core.auth.utils import VerifyToken

router = APIRouter()
token_verifier = VerifyToken()

@router.get("/", status_code=status.HTTP_200_OK)
def health(auth_result: str = Security(token_verifier.verify)) -> Any:
    print(auth_result)
    return {"status": "Running"}