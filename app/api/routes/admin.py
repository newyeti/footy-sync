from typing import Any

from fastapi import APIRouter, status, Security, Response
from app.core.auth.utils import VerifyToken
from prometheus_client import REGISTRY
from prometheus_client.openmetrics.exposition import (CONTENT_TYPE_LATEST,
                                                      generate_latest)

router = APIRouter()
token_verifier = VerifyToken()

@router.get("/", status_code=status.HTTP_200_OK)
def health(auth_result: str = Security(token_verifier.verify)) -> Any:
    return {"status": "Running"}

@router.get("/metrics")
def api_metrics(auth_result: str = Security(token_verifier.verify)) -> Any:
    return Response(generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST})

