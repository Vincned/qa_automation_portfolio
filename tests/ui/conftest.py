import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
import allure

@pytest.fixture(scope='session')
def browser():
    #launch sync_playwright for browser control
    with sync_playwright() as p:
        #launch chrominium without displaying the browser window
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope='function')
def context(browser):
    #context creation
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture(scope='function')
def page(context):
    #page creation
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def login_page(page):
    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #create the test result before yield
    outcome = yield
    report = outcome.get_result()

    #report.when == "call" - react on the error while test run and not error while configuring fixture or teardown
    #report.failed - check that the test fail
    if report.when == "call" and report.failed:
        # get the page object from the fixtures
        page = item.funcargs.get("page")

        if page:
            #attach the image to the report
            allure.attach(
                page.screenshot(),
                name="Screenshot on failure",
                attachment_type=allure.attachment_type.PNG,
            )
