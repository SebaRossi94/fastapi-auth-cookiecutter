from fastapi.testclient import TestClient

def test_home(app):
    client = TestClient(app)
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert "application_up" in response.json().keys()
    assert "database_up" in response.json().keys()
    assert "settings" in response.json().keys()
    assert isinstance(response.json()["settings"], dict)
    assert response.json()["settings"]["app_env"] == "test"
    assert response.json()["settings"]["sql_alchemy_database_url"] == "sqlite:///db.sqlite"
    assert response.json()["database_up"] == True