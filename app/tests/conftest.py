import pytest
from asgi_lifespan import LifespanManager
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import settings
from app.main import app
from app.models import ProductWrite


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(name="jwt_token")
async def get_jwt_token_fixture(client: AsyncClient):
    result = await client.post(
        url="/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": settings.admin_username,
            "password": settings.admin_password,
        },
    )
    yield result.json()["access_token"]


@pytest.fixture(name="client", scope="session")
async def async_app_client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost") as client:
            yield client


async def mock_create_product(
    client: AsyncClient, jwt_token: str = "nothing", name: str = "Test product"
):
    response = await client.post(
        url="/products",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json=ProductWrite(name=name, description="Test description").dict(),
    )
    return response
