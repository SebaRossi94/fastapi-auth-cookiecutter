from fastapi.testclient import TestClient


def test_healthcheck_with_db(app_with_db):
    client = TestClient(app_with_db)
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert "application_up" in response.json().keys()
    assert "database_up" in response.json().keys()
    assert "settings" in response.json().keys()
    assert isinstance(response.json()["settings"], dict)
    assert response.json()["settings"]["app_env"] == "test"
    assert (
        response.json()["settings"]["sql_alchemy_database_url"] == "sqlite:///db.sqlite"
    )
    assert response.json()["database_up"] is True


def test_healthcheck_without_db(app_without_db):
    client = TestClient(app_without_db)
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert "application_up" in response.json().keys()
    assert "database_up" in response.json().keys()
    assert "settings" in response.json().keys()
    assert isinstance(response.json()["settings"], dict)
    assert response.json()["settings"]["app_env"] == "test"
    assert (
        response.json()["settings"]["sql_alchemy_database_url"] == "sqlite:///db.sqlite"
    )
    print(response.json())
    assert response.json()["database_up"] is False
