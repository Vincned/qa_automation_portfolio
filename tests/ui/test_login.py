from playwright.sync_api import expect
from pages.login_page import LoginPage
import pytest
import allure


@allure.title("Successful login")
@allure.description("Verify that a user can log in with valid credentials")
def test_login(login_page):
    with allure.step("Enter credentials"):
        login_page.login("tomsmith", "SuperSecretPassword!")
    #check the heading
    with allure.step("Verify successful login"):
        expect(login_page.secure_area_heading).to_be_visible()


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
