import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def api_client(request):
    from main import app
    yield TestClient(app)
