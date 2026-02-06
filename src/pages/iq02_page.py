from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class IQ02Page(BasePage):

    INPUT_MATERIAL = (By.XPATH, "//input[@role='textbox' and @title='Número de material']")
    INPUT_NSE = (By.XPATH, "//input[@role='textbox' and @title='Número de serie']")
    INPUT_ALMACEN = (By.XPATH, "//input[@role='textbox' and @title='Almacén']")

    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout)
        
    def set_material(self, material: str) -> None:
        self.write(self.INPUT_MATERIAL, material)

    def set_nse(self, nse: str) -> None:
        self.write(self.INPUT_NSE, nse)

    def set_option(self, option: str) -> None:
        option_locator = (By.XPATH, f"//span[@role='radio' and @title='{option}']")
        ok_button_locator = (By.XPATH, "//div[@role='button' and @title='Continuar (Entrada)']")
        self.click(option_locator, allow_js_fallback=True)
        self.click(ok_button_locator)
    
    def set_almacen(self, almacen: str) -> None:
        self.write(self.INPUT_ALMACEN, almacen)

    
    