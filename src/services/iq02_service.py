from src.pages.iq02_page import IQ02Page
from selenium.common.exceptions import TimeoutException
import time

class IQ02Service:

    def __init__(self, driver, timeout: int = 10):
        self.page = IQ02Page(driver, timeout)

    def open(self) -> None:
        self.page.wait_for_okcode()
        self.page.toolbar.enter_command("/nIQ02")

    def run(self, material: str | None = None, nse: str | None = None) -> dict:
        if material:
            self.page.set_material(material)
        if nse:
            self.page.set_nse(nse)
        
        self.page.press_enter()

        return {
            "status_text": self.page.statusbar.get().text,
        }
    
    def enter_data(self, material: str, nse: str) -> None:
        self.page.set_material(material)
        self.page.set_nse(nse)
        self.page.press_enter()

    def open_operacion_manual_num_serie(self) -> None:
        self.page.toolbar.open_operacion_manual_num_serie()

    def select_operacion_manual_option(self, option: str) -> None:
        self.page.set_option(option)
        time.sleep(3)
    
    def set_almacen(self, almacen: str) -> None:
        self.page.set_almacen(almacen)

    def save(self) -> None:
        self.page.toolbar.save()
    
    def exit(self) -> None:
        try:
            self.page.toolbar.end()
            self.page.wait_for_okcode()
        except TimeoutException:
            pass