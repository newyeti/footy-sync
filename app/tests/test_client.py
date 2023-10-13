from unittest import mock

import pytest
from httpx import AsyncClient

from ..main import app, container
from ..dependencies.services import Service


@pytest.fixture
def client(event_loop):
    client = AsyncClient(app=app, base_url="http://localhost")
    yield client
    event_loop.run_until_complete(client.aclose())

@pytest.mark.asyncio
async def test_redis_client(client):
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.redis_conn_test.return_value = "success"
    
    with container.service.override(service_mock):
        response = await client.get("/connect/test/redis")
    
    assert response.status_code == 200
    assert response.json() == {'connection': 'success'}
