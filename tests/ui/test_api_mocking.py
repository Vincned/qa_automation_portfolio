from playwright.async_api import expect
import pytest

def mock_json_error(route):
    route.fulfill(
        status=500,
        content_type="application/json",
        body='{"error": "Internal Server Error", "message": "Something went wrong"}'
    )

def test_mock_json_response(login_page):
    login_page.page.route("**/api/test", mock_json_error)
    result = login_page.page.evaluate("""
    async () => {
        const response = await fetch("/api/test", {
            method: "GET"
        });

        return {
            status: response.status,
            data: await response.json()
        };
    }
""")
    assert result["status"] == 500
    assert result["data"]["error"] == "Internal Server Error"


def mock_network_error(route):
    route.abort()

def test_api_network_failure(login_page):
    login_page.page.route("**/api/test", mock_network_error)
    
    result = login_page.page.evaluate("""
        async () => {
            try {
                const response = await fetch("/api/test");
                return { failed: false };
            } catch (error) {
                return { failed: true };
            }
        }
    """)

    assert result['failed'] is True
