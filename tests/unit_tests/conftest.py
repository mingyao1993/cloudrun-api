import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def api_client(request):
    """Generate an API test client

    Need to parametrize with a ScheduleModeEnum member, eg:
       @pytest.mark.parametrize("api_client", [ScheduleModeEnum.ALWAYS_ON], indirect=True)
    """
    os.environ["APPLICATION_NAME"] = "test-api"

    from main import app

    yield TestClient(app)
