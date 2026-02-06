from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.config import settings

class LoginPage(BasePage):

    USERNAME = (By.ID, "sap-user")
    PASSWORD = (By.ID, "sap-password")
    LOGIN_BUTTON = (By.ID, "LOGON_BUTTON")
    USE_SAP_FRAME = False

    def __init__(self, driver, timeout: int = 15):
        super().__init__(driver, timeout)

    def open_login_page(self) -> None:
        self.open_url(settings.SAP_LOGIN_URL)

    def login(self, username, password) -> None:
        self.write(self.USERNAME, username)
        self.write(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

        self.USE_SAP_FRAME = True