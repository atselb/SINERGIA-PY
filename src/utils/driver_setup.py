import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def create_driver():
    # Inicializar el naegador Chrome usando Webdriver Manager
    chrome_options = Options()

    # Configuraciones adicionales del navegador
    chrome_options.add_argument("--incognito")

    # Evitar popups de Chrome
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.password_manager_leak_detection": False,
        "signin.allowed": False 
    }

    chrome_options.add_experimental_option("prefs", prefs)

    # Evitar log
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.maximize_window()

    return driver