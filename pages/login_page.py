class LoginPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://the-internet.herokuapp.com/login"
        self.username = self.page.get_by_label("Username")
        self.password = self.page.get_by_label("Password")
        self.login_button = self.page.get_by_role("button")
        self.secure_area_heading = self.page.get_by_role(
            "heading", name="Secure Area", exact=True
        )
        self.error_message = self.page.locator("#flash")

    def open(self):
        self.page.goto(self.url)

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
