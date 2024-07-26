from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from python_dev_environment.database import Base
from python_dev_environment.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"  # in-memory database

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def setup_database():
    with TestingSessionLocal() as db:
        Base.metadata.create_all(bind=engine)
        yield db
        Base.metadata.drop_all(bind=engine)


def test_create_and_get_player(setup_database):
    USER_NAME = "my new user"
    response = client.put("/user", json={"name": USER_NAME})
    assert response.status_code == 200
    user_id = response.json()["id"]
    assert response.json()["name"] == USER_NAME

    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "name": USER_NAME}
