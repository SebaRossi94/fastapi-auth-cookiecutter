from fastapi.testclient import TestClient
from app.tests.conftest import fake_users


def test_auth_token_success(app_with_db):
    client = TestClient(app_with_db)
    login_data = {"username": fake_users["darth"].email, "password": "Anakin"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    login_response = client.post("auth/token", data=login_data, headers=headers)
    print(login_response.json())
    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert "access_token" in login_response.json().keys()


def test_auth_token_error(app_with_db):
    client = TestClient(app_with_db)
    login_data = {"username": "jointhelightside@rebels.com", "password": "Luke"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    login_response = client.post("auth/token", data=login_data, headers=headers)
    print(login_response.json())
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid credentials"
