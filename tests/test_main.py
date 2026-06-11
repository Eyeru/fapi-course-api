from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello Backend"
    }


def test_login():
    response = client.post(
        "/auth/token",
        data={
            "username": "pt",
            "password": "1234"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


def test_get_courses():
    response = client.get("/courses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_course(admin_token):

    course_data = {
        "name": "Software Engineering",
        "credit": 3
    }

    response = client.post(
        "/courses",
        json=course_data,
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Software Engineering"
    assert data["credit"] == 3


def test_student_cannot_delete_course(student_token):

    response = client.delete(
        "/courses/1",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert response.status_code == 403


def test_admin_can_delete_course(admin_token):

    create_response = client.post(
        "/courses",
        json={
            "name": "Temporary Course",
            "credit": 3
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    course_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/courses/{course_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert delete_response.status_code == 200