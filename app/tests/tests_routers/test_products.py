import pytest
from httpx import AsyncClient

from app.main import app
from app.models.product_model import ProductWrite
from app.tests.conftest import mock_create_product

# from app.tests.conftest import mock_create_product


@pytest.mark.anyio
async def test_create_product(jwt_token: str, client: AsyncClient):
    response = await mock_create_product(jwt_token=jwt_token, client=client)
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Test product"
    assert data["description"] == "Test description"


@pytest.mark.anyio
async def test_create_product_invalid_token(client: AsyncClient):
    response = await mock_create_product(client=client)
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Invalid token"


@pytest.mark.anyio
async def test_create_product_no_token(client: AsyncClient):
    response = await client.post(
        url="/products",
        json=ProductWrite(
            name="Test name", description="Test description"
        ).dict(),
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Not authenticated"


@pytest.mark.anyio
async def test_create_product_incomplete_body(
    jwt_token: str, client: AsyncClient
):
    response = await client.post(
        url="/products",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )

    data = response.json()
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_product_exists_already(
    jwt_token: str, client: AsyncClient
):
    await mock_create_product(jwt_token=jwt_token, client=client, name="Test 2")
    response = await mock_create_product(
        jwt_token=jwt_token, client=client, name="Test 2"
    )
    data = response.json()
    assert data["detail"] == "Product already exists"
    assert response.status_code == 400


@pytest.mark.anyio
async def test_update_product_description(jwt_token: str, client: AsyncClient):
    await mock_create_product(jwt_token=jwt_token, client=client, name="Test 3")
    response = await client.patch(
        url="/products/3",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test 3"
    assert data["description"] == "Test description edited"


@pytest.mark.anyio
async def test_update_product_description_not_existing(
    jwt_token: str, client: AsyncClient
):
    await mock_create_product(jwt_token=jwt_token, client=client, name="Test 4")
    response = await client.patch(
        url="/products/5",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )
    data = response.json()
    assert response.status_code == 404


@pytest.mark.anyio
async def test_delete_product(jwt_token: str, client: AsyncClient):
    await mock_create_product(jwt_token=jwt_token, client=client, name="Test 5")
    response = await client.delete(
        url="/products/5",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert response.status_code == 200
    response = await client.patch(
        url="/products/5",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_product(jwt_token: str, client: AsyncClient):
    await mock_create_product(jwt_token=jwt_token, client=client, name="Test 6")
    response = await client.get(
        url="/products/6", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test 6"
    assert data["description"] == "Test description"


@pytest.mark.anyio
async def test_get_product_not_existing(jwt_token: str, client: AsyncClient):
    await mock_create_product(jwt_token=jwt_token, client=client)
    response = await client.get(
        url="/products/7", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 404


# def test_get_products(jwt_token: str, client: AsyncClient):
#     mock_create_product(jwt_token=jwt_token, client=client)
#     mock_create_product(
#         jwt_token=jwt_token, client=client, name="Test product 2"
#     )
#     response = client.get(
#         url="/products", headers={"Authorization": f"Bearer {jwt_token}"}
#     )
#     data = response.json()
#     assert response.status_code == 200
#     assert data[0]["name"] == "Test product"
#     assert data[0]["description"] == "Test description"
#     assert data[1]["name"] == "Test product 2"
#     assert data[1]["description"] == "Test description"
