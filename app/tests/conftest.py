import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.config.config import settings
from app.db.database import get_session
from app.main import app
from app.models.product_model import ProductWrite


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="jwt_token")
def get_jwt_token_fixture(client: TestClient):
    yield client.post(
        url="/login",
        headers={"Content-Type": "application/json"},
        json={
            "username": settings.admin_username,
            "password": settings.admin_password,
        },
    ).json()["access_token"]


def mock_create_product(
    jwt_token: str, client: TestClient, name: str = "Test product"
):
    return client.post(
        url="/products",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json=ProductWrite(name=name, description="Test description").dict(),
    )
