from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ToolbarComponent():

    COMMAND_INPUT = (By.ID, "ToolbarOkCode")

    BTN_BACK = (By.XPATH, "//div[@role='button' and @title='Atrás (F3)']")
    BTN_END = (By.XPATH, "//div[@role='button' and @title='Finalizar (Mayús+F3)']")
    BTN_CANCEL = (By.XPATH, "//div[@role='button' and @title='Cancelar (Escape)']")
    BTN_SAVE = (By.XPATH, "//div[@role='button' and (@title='Contabilizar (Ctrl+S)' or @title='Grabar (Ctrl+S)')]")
    BTN_MENU = (By.XPATH, "//div[@role='button' and @title='Menú']")

    def __init__(self, page):
        self.page = page

    def enter_command(self, command: str) -> None:
        self.page.write(self.COMMAND_INPUT, command)
        self.page.press_enter()

    def back(self) -> None:
        self.page.click(self.BTN_BACK)
    def end(self) -> None:
        self.page.click(self.BTN_END)

    def cancel(self) -> None:
        self.page.click(self.BTN_CANCEL)

    def save(self) -> None:
        self.page.click(self.BTN_SAVE)

    def open_operacion_manual_num_serie(self) -> None:
        self.page.press_key_combo(Keys.CONTROL, Keys.SHIFT, Keys.F2)