import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pathlib import Path
import allure
from requests import request


@pytest.fixture(scope='session')
def browser(worker_id):
    #launch sync_playwright for browser control
    with sync_playwright() as p:
        #launch chrominium without displaying the browser window
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope='function')
def context(browser, request):
    #context creation
    context = browser.new_context()

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    try:
        yield context

    finally:
        try:
            report = getattr(request.node, "rep_call", None)

            if report and report.failed:
                trace_dir = Path("test-results")
                trace_dir.mkdir(parents=True, exist_ok=True)

                trace_path = trace_dir / f"{request.node.name}.zip"
                context.tracing.stop(path=str(trace_path))
            else:
                context.tracing.stop()
        finally:
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


@pytest.fixture
def two_contexts(browser):
    context1 = browser.new_context()

    try:
        context2 = browser.new_context()

        try:
            yield context1, context2
        finally:
            context2.close()

    finally:
        context1.close()

@pytest.fixture
def valid_credentials():
    valid_data = {"username": "tomsmith", "password": "SuperSecretPassword!"}

    return valid_data

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    #create the test result before yield
    outcome = yield
    report = outcome.get_result()

     # Save the report so fixtures can access the test result.
    setattr(item, f"rep_{report.when}", report)

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


@pytest.fixture(scope="function")
def authenticated_page(page):
    api_request = page.context.request
    response = api_request.post(
        "https://the-internet.herokuapp.com/authenticate",
        form={
            "username": "tomsmith",
            "password": "SuperSecretPassword!",
        }
    )
    assert response.status == 200
    assert response.url == "https://the-internet.herokuapp.com/secure"

    page.goto("https://the-internet.herokuapp.com/secure")

    return page
