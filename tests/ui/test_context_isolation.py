from playwright.sync_api import expect
from pages.login_page import LoginPage
import pytest

def test_contexts_are_isolated(two_contexts):
    context1, context2 = two_contexts

    context1.add_cookies([
    {
        "name": "session_id",
        "value": "user1",
        "url": "https://example.com"
    }
])

    cookie1 = context1.cookies()
    cookie2 = context2.cookies()

    assert any(cookie["name"] == "session_id" for cookie in cookie1)
    assert not any(cookie["name"] == "session_id" for cookie in cookie2)

def test_authenticated_contexts_are_isolated(two_contexts, valid_credentials):
    context1, context2 = two_contexts

    page1 = context1.new_page()
    page2 = context2.new_page()

    login_page1 = LoginPage(page1)
    login_page1.open()
    login_page1.login(
        valid_credentials['username'],
        valid_credentials['password']
    )

    login_page2 = LoginPage(page2)

    #try to enter to the secure area without auth
    page2.goto("https://the-internet.herokuapp.com/secure")

    #check that the title secure area is visible for context1
    expect(login_page1.secure_area_heading).to_be_visible()
    #back to the login page without auth for context2
    expect(page2).to_have_url("https://the-internet.herokuapp.com/login")
    #field login must be visible on the page2
    expect(login_page2.username).to_be_visible()
    #the context1 is still auth
    expect(login_page1.secure_area_heading).to_be_visible()
