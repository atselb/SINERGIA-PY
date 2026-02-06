from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class BasePage:

    USE_SAP_FRAME = True
    SAP_FRAME = (By.ID, "ITSFRAME1")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

        from src.pages.components.toolbar_component import ToolbarComponent
        from src.pages.components.statusbar_component import StatusbarComponent
        self.toolbar = ToolbarComponent(self)
        self.statusbar = StatusbarComponent(self)

    # Métodos de acción

    def open_url(self, url) -> None:
        self.driver.get(url)
    
    def switch_to_sap(self) -> None:
        if not self.USE_SAP_FRAME:
            return
        
        for i in range(3):
            try:
                self.driver.switch_to.default_content()
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.SAP_FRAME))
                return
            except StaleElementReferenceException:
                if i == 2:
                    raise
        
    def _retry_on_stale(self, fn, attempts: int = 3):
        for i in range(attempts):
            try:
                self.switch_to_sap()
                return fn()
            except StaleElementReferenceException:
                if i == attempts - 1:
                    raise

    def click(self, locator, allow_js_fallback: bool = False) -> None:
        def _do():
            el = self.wait.until(EC.visibility_of_element_located(locator))
            try:
                el.click()
            except Exception:
                if not allow_js_fallback:
                    raise
                self.driver.execute_script("arguments[0].click();", el)

        self._retry_on_stale(_do)
        
    def write(self, locator, text) -> None:
        def _do():
            el = self.wait.until(EC.element_to_be_clickable(locator))
            el.click()
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.BACKSPACE)
            el.send_keys(text)

        self._retry_on_stale(_do)

    def get_text(self, locator) -> str:
        element = self.find(locator)
        return element.text

    def find(self, locator) -> any:
        def _do():
            return self.wait.until(EC.presence_of_element_located(locator))
        return self._retry_on_stale(_do)
    
    def press_enter(self) -> None:
        self.switch_to_sap()
        self.driver.switch_to.active_element.send_keys(Keys.RETURN)

    def press_key_combo(self, *keys: Keys) -> None:
        self.switch_to_sap()
        body = self.driver.find_element(By.TAG_NAME, "body")
        body.click()

        actions = ActionChains(self.driver)

        for key in keys[:-1]:
            actions.key_down(key)

        actions.send_keys(keys[-1])

        for key in reversed(keys[:-1]):
            actions.key_up(key)

        actions.perform()

    def exists(self, locator) -> bool:
        try:
            self.find(locator)
            return True
        except TimeoutException:
            return False
        
    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_okcode(self) -> None:

        locator = self.toolbar.COMMAND_INPUT
        assert isinstance(locator, tuple), f"COMMAND_INPUT debe ser una tupla, llegó {type(locator)}"

        def _do():
            self.switch_to_sap()
            self.wait.until(EC.element_to_be_clickable(locator))

        self._retry_on_stale(_do)

    def switch_to_popup(self) -> None:
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.SAP_FRAME))
