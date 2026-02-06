from src.pages.login_page import LoginPage
from src.config import settings

class LoginService:

    def __init__(self, driver):
        self.page = LoginPage(driver)

    def ensure_logged_in(self):
        self.page.open_login_page()

        if self.page.is_visible(self.page.USERNAME):
            self.page.login(
                settings.SAP_USERNAME,
                settings.SAP_PASSWORD
            )

        if self.page.is_visible(self.page.USERNAME):
            raise RuntimeError("Login falló: el formulario sigue visible")