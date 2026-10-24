import requests

class APIClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.request(
            method=method,
            url=url,
            headers=self.headers,
            timeout=self.timeout,
            **kwargs,
        )


    def get(self, endpoint):
        return self._request("GET", endpoint)

    def post(self, endpoint, data):
        return self._request("POST", endpoint, json=data)

    def put(self, endpoint, data):
        return self._request("PUT", endpoint, json=data)

    def patch(self, endpoint, data):
        return self._request("PATCH", endpoint, json=data)

    def delete(self, endpoint):
        return self._request("DELETE", endpoint)
