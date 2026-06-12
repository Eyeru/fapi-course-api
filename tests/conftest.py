import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from tests.test_database import override_get_db
from app.models.user import User
from app.core.security import hash_password
from tests.test_database import engine, TestingSessionLocal


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def admin_token():

    db = TestingSessionLocal()

    existing = db.query(User).filter(
        User.username == "test_admin"
    ).first()

    if not existing:

        admin = User(
            username="test_admin",
            email="admin@test.com",
            hashed_password=hash_password("1234"),
            role="admin"
        )

        db.add(admin)
        db.commit()

    db.close()

    response = client.post(
        "/auth/token",
        data={
            "username": "test_admin",
            "password": "1234"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def student_token():

    db = TestingSessionLocal()

    existing = db.query(User).filter(
        User.username == "test_student"
    ).first()

    if not existing:

        student = User(
            username="test_student",
            email="student@test.com",
            hashed_password=hash_password("1234"),
            role="student"
        )

        db.add(student)
        db.commit()

    db.close()

    response = client.post(
        "/auth/token",
        data={
            "username": "test_student",
            "password": "1234"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def db():

    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()