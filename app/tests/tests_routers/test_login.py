import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import settings


@pytest.mark.anyio
async def test_login(client: AsyncClient):
    response = await client.post(
        url="/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": settings.admin_username,
            "password": settings.admin_password,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "Bearer"
    assert data["message"] == "Admin logged in"


@pytest.mark.anyio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        url="/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": "invalid",
            "password": settings.admin_password,
        },
    )
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "Incorrect email or password"
