from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Product
from app.tests.conftest import mock_create_product
from app.utils import get_offers, register_product


def test_register_product():
    product = Product(name="Test product", description="Test description")
    result = register_product(product)
    assert result == True


def test_get_offers(jwt_token: str, client: TestClient, session: Session):
    mock_create_product(jwt_token=jwt_token, client=client)
    assert get_offers(session=session) == True
