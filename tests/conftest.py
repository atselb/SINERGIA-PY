import pytest
from dotenv import load_dotenv

from src.utils.driver_setup import create_driver
from src.services.login_service import LoginService
from src.pages.base_page import BasePage

load_dotenv()

@pytest.fixture(scope="session")
def driver():
    driver = create_driver()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def sap_session(driver):
    login_service = LoginService(driver)
    login_service.ensure_logged_in()
    return driver

# Revisar. Posible discontinuado.
@pytest.fixture(scope="session")
def app(sap_session):
    return BasePage(sap_session)