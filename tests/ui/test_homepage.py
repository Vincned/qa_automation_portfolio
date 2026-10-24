from playwright.sync_api import expect

def test_example_page(page):
    page.goto("https://the-internet.herokuapp.com/")

    expect(page.locator("h1")).to_have_text("Welcome to the-internet")
    expect(page).to_have_title("The Internet")
