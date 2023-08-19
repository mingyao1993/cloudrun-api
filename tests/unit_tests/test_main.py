import base64
import json
from unittest.mock import patch

from cloud.datastore import Datastore


def test_health(api_client):
    """
    WHEN reading from the ping endpoint
    THEN a basic response will be received
    """
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}


@patch.object(target=Datastore, attribute='transfer_funds', return_value=None)
def test_transfer_funds_success(mock_transfer_funds, api_client):
    transfer_funds_request = {"from": "q1w2e3", "to": "r4t5y6", "amount": 50}
    request_body = {
        "message": {
            "data": base64.b64encode(json.dumps(transfer_funds_request).encode('utf-8')).decode('utf-8'),
            "messageId": "123",
            "publishTime": "2023-01-01T00:00:00.000000Z"
        }
    }
    response = api_client.post("/v1/transfer_funds", json=request_body)
    assert response.status_code == 200
    assert response.json() == {'message_id': '123'}
