from fastapi.testclient import TestClient

from app.models.product_model import ProductWrite
from app.tests.conftest import mock_create_product


def test_create_product(jwt_token: str, client: TestClient):
    response = mock_create_product(jwt_token=jwt_token, client=client)
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test product"
    assert data["description"] == "Test description"


def test_create_product_no_login(client: TestClient):
    response = client.post(
        url="/products",
        json=ProductWrite(
            name="Test product", description="Test description"
        ).dict(),
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Not authenticated"


def test_create_product_incomplete_body(jwt_token: str, client: TestClient):
    response = client.post(
        url="/products",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )

    data = response.json()
    assert response.status_code == 422


def test_create_product_exists_already(jwt_token: str, client: TestClient):
    mock_create_product(jwt_token=jwt_token, client=client)
    response = client.post(
        url="/products",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json=ProductWrite(
            name="Test product", description="Test description"
        ).dict(),
    )
    data = response.json()
    assert data["detail"] == "Product already exists"
    assert response.status_code == 406


def test_update_product_description(jwt_token: str, client: TestClient):
    mock_create_product(jwt_token=jwt_token, client=client)
    response = client.patch(
        url="/products/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test product"
    assert data["description"] == "Test description edited"


def test_update_product_description_not_existing(
    jwt_token: str, client: TestClient
):
    mock_create_product(jwt_token=jwt_token, client=client)
    response = client.patch(
        url="/products/2",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )
    data = response.json()
    assert response.status_code == 404


def test_delete_product(jwt_token: str, client: TestClient):
    mock_create_product(jwt_token=jwt_token, client=client)
    response = client.delete(
        url="/products/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert response.status_code == 200
    response = client.patch(
        url="/products/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"description": "Test description edited"},
    )
    assert response.status_code == 404


def test_get_product(jwt_token: str, client: TestClient):
    mock_create_product(jwt_token=jwt_token, client=client)
    response = client.get(
        url="/products/1", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test product"
    assert data["description"] == "Test description"


def test_get_product_not_existing(jwt_token: str, client: TestClient):
    mock_create_product(jwt_token=jwt_token, client=client)
    response = client.get(
        url="/products/2", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response.status_code == 404


def test_get_products(jwt_token: str, client: TestClient):
    mock_create_product(jwt_token=jwt_token, client=client)
    mock_create_product(
        jwt_token=jwt_token, client=client, name="Test product 2"
    )
    response = client.get(
        url="/products", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data[0]["name"] == "Test product"
    assert data[0]["description"] == "Test description"
    assert data[1]["name"] == "Test product 2"
    assert data[1]["description"] == "Test description"
