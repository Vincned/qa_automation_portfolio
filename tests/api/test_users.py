import pytest
import requests
from unittest.mock import patch

@pytest.mark.parametrize(
        "user_id, expected_status",
        [
            (1, 200),
            (2, 200),
            (3, 200),
        ]
)
def test_get_user(api_client, user_id, expected_status):
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code == expected_status

    user = response.json()

    assert isinstance(user, dict)

    assert "id" in user
    assert user["id"] == user_id
    assert isinstance(user["id"], int)

    assert "name" in user
    assert isinstance(user["name"], str)
    assert user["name"]

    assert "email" in user
    assert isinstance(user["email"], str)
    assert user["email"]


@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (-1, 404),
        (0, 404),
        (9999, 404),
    ],
)

def test_get_nonexistent_user(api_client, user_id, expected_status):
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code == expected_status
    assert response.json() == {}

def test_api_timeout(api_client):
    with patch(
        "client.api_client.requests.request",
        side_effect=requests.exceptions.Timeout,
    ):
        with pytest.raises(requests.exceptions.Timeout):
            api_client.get("/users/1")

def test_api_connection_error(api_client):
    with patch(
        "client.api_client.requests.request",
        side_effect=requests.exceptions.ConnectionError,
    ):
        with pytest.raises(requests.exceptions.ConnectionError):
            api_client.get("/users/1")
