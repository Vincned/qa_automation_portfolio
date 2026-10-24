import pytest
import requests
from unittest.mock import patch

def test_get_result_from_requests(api_client):
    fake_response = object()

    with patch(
        "client.api_client.requests.request",
        return_value=fake_response,
    ):
        result = api_client.get("/users/1")

    assert result is fake_response


    payload = {"name": "Alice", "mail": "bububu@gmail.com"}

    with patch(
        "client.api_client.requests.request",
    ) as mock_request:
        api_client.put("/users/1", payload)

    mock_request.assert_called_once_with(
        method="PUT",
        url="https://jsonplaceholder.typicode.com/users/1",
        headers=api_client.headers,
        timeout=api_client.timeout,
        json=payload,
    )


    with patch(
        "client.api_client.requests.request",
    ) as mock_request:
        api_client.delete("/users/1")

    mock_request.assert_called_once_with(
        method="DELETE",
        url="https://jsonplaceholder.typicode.com/users/1",
        headers=api_client.headers,
        timeout=api_client.timeout,
    )

@pytest.mark.parametrize("method, endpoint", [
                         ("GET", "/users/1"),
                         ("DELETE", "/users/1")
])

def test_get_and_delete_requests(api_client, method, endpoint):
    with patch(
        "client.api_client.requests.request",
    ) as mock_request:
        if method == "GET":
            api_client.get(endpoint)
        else:
            api_client.delete(endpoint)

        mock_request.assert_called_once_with(
            method=method,
            url=f"{api_client.base_url}{endpoint}",
            headers=api_client.headers,
            timeout=api_client.timeout,
        )

@pytest.mark.parametrize("method, endpoint, payload", [
                         ("POST", "/users", {"name": "Alice", "email": "alice@example.com"}),
                         ("PUT", "/users/1", {"name": "Alice", "email": "alice@example.com"}),
                         ("PATCH", "/users/1", {"name": "Alice"})
])

def test_post_put_patch_requests(api_client, method, endpoint, payload):
    with patch(
        "client.api_client.requests.request",
    ) as mock_request:

        if method == "POST":
            api_client.post(endpoint, payload)
        elif method == "PUT":
            api_client.put(endpoint, payload)
        else:
            api_client.patch(endpoint, payload)

        mock_request.assert_called_once_with(
            method=method,
            url=f"{api_client.base_url}{endpoint}",
            headers=api_client.headers,
            timeout=api_client.timeout,
            json=payload
        )
