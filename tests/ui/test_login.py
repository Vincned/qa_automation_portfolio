from playwright.sync_api import expect
from tests.test_data.login_data import TEST_CASES
import pytest
import allure


@allure.title("Successful login")
@allure.description("Verify that a user can log in with valid credentials")
def test_login(login_page, valid_credentials):
    with allure.step("Enter credentials"):
        with login_page.page.expect_response(
            lambda response: (
                response.url.endswith("/authenticate") and
                response.request.method == "POST"
            )
        ) as response_info:

            with login_page.page.expect_request(
                lambda request: (
                    request.url.endswith("/secure") and 
                    request.method == "GET"
                )
            ) as request_info:
                
                with login_page.page.expect_response(
                    lambda response: (
                        response.url.endswith("/secure") and
                        response.request.method == "GET"
                    )
                ) as secure_response_info:
                    
                    login_page.login(
                        valid_credentials["username"],
                        valid_credentials["password"]
                        )

        secure_response = secure_response_info.value
        assert secure_response.status == 200
        assert secure_response.url.endswith("/secure")
    
        request = request_info.value
        headers = request.all_headers()
        assert "cookie" in headers

    #check the heading
    with allure.step("Verify successful login"):
        expect(login_page.secure_area_heading).to_be_visible()

    response = response_info.value
    assert response.headers.get("location") == "https://the-internet.herokuapp.com/secure"
    assert response.status == 303


def test_login_via_api(authenticated_page):
    assert authenticated_page.url.endswith('/secure')


def test_authenticated_page(authenticated_page):
    expect(authenticated_page.get_by_role("heading", name="Secure Area", exact=True))


def mock_server_error(route):
    route.fulfill(
    status=500,
    content_type="text/html",
    body="<html><body><h1>Mock server error</h1></body></html>",
    );


def test_login_error(login_page):
    login_page.page.route("**/authenticate", mock_server_error)
    login_page.login("tomsmith", "SuperSecretPassword!")

    expect(login_page.page.get_by_role("heading", name="Mock server error")).to_be_visible()


@pytest.mark.parametrize(
    "username_value, password_value, error_value",
    TEST_CASES
    )

def test_login_invalid_credentials(login_page, username_value, password_value, error_value):
    
    login_page.login(username_value, password_value)
    #error check
    expect(login_page.error_message).to_contain_text(error_value)
    expect(login_page.username).to_be_visible()
    expect(login_page.password).to_be_visible()
    expect(login_page.page).to_have_url(login_page.url)
