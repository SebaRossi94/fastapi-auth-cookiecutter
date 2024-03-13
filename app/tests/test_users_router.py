from unittest.mock import patch
from fastapi.testclient import TestClient

from app.tests.conftest import fake_users


def test_me_success(app_with_db_and_jwt):
    client = TestClient(app_with_db_and_jwt)
    me_response = client.get("/users/me")
    print(me_response.json())
    assert me_response.status_code == 200
    assert me_response.json()["id"] == 1
    assert me_response.json()["email"] == fake_users["darth"].email


def test_me_no_auth(app_with_db):
    client = TestClient(app_with_db)
    me_response = client.get("/users/me")
    assert me_response.status_code == 401
    assert me_response.json()["detail"] == "Not authenticated"


def test_get_all_users_success(app_with_db):
    client = TestClient(app_with_db)
    me_response = client.get("/users/all")
    assert me_response.status_code == 200
    assert isinstance(me_response.json(), list)


def test_get_user_by_id_success(app_with_db):
    client = TestClient(app_with_db)
    me_response = client.get("/users/1")
    assert me_response.status_code == 200
    assert me_response.json()["id"] == 1
    assert me_response.json()["email"] == fake_users["darth"].email
    assert me_response.json()["first_name"] == fake_users["darth"].first_name


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
    assert create_user_response.status_code == 201
    assert create_user_response.json()["email"] == user_data["email"]
    assert "password" not in create_user_response.json().keys()
    assert create_user_response.json()["first_name"] == user_data["first_name"]
    assert create_user_response.json()["last_name"] == user_data["last_name"]
    assert "id" in create_user_response.json().keys()


def test_patch_user_success(app_with_db):
    user_data = {
        "first_name": "first",
        "last_name": "last",
    }
    headers = {"Content-Type": "application/json"}
    client = TestClient(app_with_db)
    patch_user_response = client.patch("/users/1", json=user_data, headers=headers)
    assert patch_user_response.status_code == 200
    assert patch_user_response.json()["email"] == fake_users["darth"].email
    assert "password" not in patch_user_response.json().keys()
    assert patch_user_response.json()["first_name"] == user_data["first_name"]
    assert patch_user_response.json()["last_name"] == user_data["last_name"]
    assert "id" in patch_user_response.json().keys()


def test_create_user_already_exists(app_with_db):
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
    assert create_user_response.status_code == 409
    assert create_user_response.json()["detail"] == "User already exists"


def test_delete_user_by_id_success(app_with_db):
    client = TestClient(app_with_db)
    me_response = client.delete("/users/1")
    assert me_response.status_code == 204


def test_delete_user_by_id_fails(app_with_db):
    client = TestClient(app_with_db)
    me_response = client.delete("/users/100")
    assert me_response.status_code == 404
    assert me_response.json()["detail"] == "User not found"
