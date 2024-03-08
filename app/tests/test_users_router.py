from fastapi.testclient import TestClient

from app.tests.conftest import fake_users


# def test_me_success(app_with_db_and_jwt):
#     darth_user = fake_users["darth"]
#     client = TestClient(app_with_db_and_jwt)
#     headers = {"Authorization": "Bearer fakejwt.super.fake"}
#     me_response = client.get("/users/me", headers=headers)
#     print(me_response.json())
#     assert me_response.status_code == 200

def test_me_no_auth(app_with_db):
    client = TestClient(app_with_db)
    me_response = client.get("/users/me")
    print(me_response.json())
    assert me_response.status_code == 401
    assert me_response.json()["detail"] == "Not authenticated"


def test_create_user_success(app_with_db):
    user_data = {
        "email": "user@example.com",
        "password": "password",
        "first_name": "first",
        "last_name": "last"
    }
    headers = {"Content-Type": "application/json"}
    client = TestClient(app_with_db)
    create_user_response = client.post("/users/", json=user_data, headers=headers)
    print(create_user_response.json())
    assert create_user_response.status_code == 201
    assert create_user_response.json()["email"] == user_data["email"]
    assert "password" not in create_user_response.json().keys()
    assert create_user_response.json()["first_name"] == user_data["first_name"]
    assert create_user_response.json()["last_name"] == user_data["last_name"]
    assert "id" in create_user_response.json().keys()

def test_create_user_already_exists(app_with_db):
    darth_user = fake_users["darth"]
    user_data = {
        "email": darth_user.email,
        "password": "password",
    }
    headers = {"Content-Type": "application/json"}
    client = TestClient(app_with_db)
    create_user_response = client.post("/users/", json=user_data, headers=headers)
    print(create_user_response.json())
    assert create_user_response.status_code == 418
    assert create_user_response.json()["detail"] == "Unhandled Error"
