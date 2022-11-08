import pytest

from app import create_app


@pytest.fixture(name="test_app")
def base_test_app():
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture(name="test_client")
def test_app_client(test_app):
    return test_app.test_client()
