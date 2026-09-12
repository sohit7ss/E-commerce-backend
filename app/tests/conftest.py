# app/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.config import settings

from sqlalchemy.engine import URL

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database="e-commerce_test",
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)   # wipe test DB clean
    Base.metadata.create_all(bind=engine) # recreate all tables fresh
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    user_data = {
        "Name": "Test User",
        "Email": "testuser@example.com",
        "Password": "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["Password"] = user_data["Password"]   # keep the plaintext password for logging in later
    return new_user


@pytest.fixture()
def token(test_user, client):
    res = client.post("/login", data={
        "username": test_user["Email"],
        "password": test_user["Password"]
    })
    assert res.status_code == 200
    login_response = res.json()
    return login_response["access_token"]


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client