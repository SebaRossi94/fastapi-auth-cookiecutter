import os
import pytest


@pytest.fixture
def app():
    os.environ.setdefault("APP_ENV", "test")
    from app.main import app

    return app
