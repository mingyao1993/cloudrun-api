def test_health(api_client):
    """
    WHEN reading from the ping endpoint
    THEN a basic response will be received
    """
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == {"health": "ok"}
