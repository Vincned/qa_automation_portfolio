from playwright.sync_api import expect

def test_add_remove(page):
    page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
    #find the "Add Element" button in the DOM
    add_button = page.get_by_role("button", name="Add Element")
    #click twice on it
    add_button.click()
    add_button.click()
    #Find the "Delete" buttons
    delete_buttons = page.get_by_role("button", name="Delete")
    #check how many buttons in the DOM
    expect(delete_buttons).to_have_count(2)
    #click only on the first button
    delete_buttons.first.click()
    #check that only one button left
    expect(delete_buttons).to_have_count(1)
