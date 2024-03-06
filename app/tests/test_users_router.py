from fastapi.testclient import TestClient

from app.tests.conftest import fake_users


def test_me_fails(app_with_db):
    darth_user = fake_users["darth"]
    client = TestClient(app_with_db)
    login_data = {"username": darth_user.email, "password": "LightSide"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    login_response = client.post("auth/token", data=login_data, headers=headers)
    print(login_response.json())
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid credentials"


def test_create_user_success(app_with_db):
    user_data = {
        "email": "user@example.com",
        "password": "password",
        "first_name": "first",
        "last_name": "last",
    }
    headers = {"Content-Type": "application/json"}
    client = TestClient(app_with_db)
    create_user_response = client.post("/users/", json=user_data, headers=headers)
    print(create_user_response.json())
    assert create_user_response.status_code == 201
    assert create_user_response.json() is None
