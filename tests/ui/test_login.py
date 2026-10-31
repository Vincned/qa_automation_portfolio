from playwright.sync_api import expect
from pages.login_page import LoginPage
import pytest
import allure


@allure.title("Successful login")
@allure.description("Verify that a user can log in with valid credentials")
def test_login(login_page):
    with allure.step("Enter credentials"):
        with login_page.page.expect_response(
            lambda response: (
                response.url.endswith("/authenticate") and
                response.request.method == "POST"
            )
        ) as response_info:
            login_page.login("tomsmith", "SuperSecretPassword!")
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

    assert login_page.page.get_by_role("heading", name="Mock server error")


@pytest.mark.parametrize(
    "username_value, password_value, error_value",
    [
        ("tomsmith", "wrong_password", "Your password is invalid!"),
        ("wrong_username", "SuperSecretPassword!", "Your username is invalid!"),
        ("wrong_username", "wrong_password", "Your username is invalid!"),
    ]
)

def test_login_invalid_credentials(login_page, username_value, password_value, error_value):
    login_page.open()
    login_page.login(username_value, password_value)
    #error check
    expect(login_page.error_message).to_contain_text(error_value)
    expect(login_page.username).to_be_visible()
    expect(login_page.password).to_be_visible()
    expect(login_page.page).to_have_url(login_page.url)
