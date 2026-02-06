import json
import re
from dataclasses import dataclass
from selenium.webdriver.common.by import By


@dataclass(frozen=True)
class StatusMessage:
    text: str
    type: str

class StatusbarComponent():

    SBAR = (By.ID, "wnd[0]/sbar_msg")
    SBAR_TEXT = (By.ID, "wnd[0]/sbar_msg-txt")
    SBAR_ICON = (By.ID, "wnd[0]/sbar_msg-icon")

    _ICON_CLASS_TO_TYPE ={
        "lsMessageBar__image--Ok": "OK",
        "lsMessageBar__image--Error": "ERROR",
        "lsMessageBar__image--Warning": "WARNING"
    }

    def __init__(self, page):
        self.page = page

    def get(self) -> StatusMessage:
        text = (self.page.get_text(self.SBAR_TEXT) or "").strip()
        msg_type = self._type_from_icon_class()
        if msg_type == "UNKNOWN":
            msg_type = self._type_from_lsdata_fallback()
        return StatusMessage(text=text, type=msg_type)

    def contains(self, substring: str) -> bool:
        return substring in self.get().text     

    def _type_from_icon_class(self) -> str:
        icon = self.page.find(self.SBAR_ICON)
        classes = (icon.get_attribute("class") or "").split()
        for cls in classes:
            if cls in self._ICON_CLASS_TO_TYPE:
                return self._ICON_CLASS_TO_TYPE[cls]
        return "UNKNOWN"
    
    def _type_from_lsdata_fallback(self) -> str:
        sbar = self.page.find(self.SBAR)
        raw = sbar.get_attribute("lsdata") or ""

        m = re.search(r"1:'([^']+)'", raw)
        if not m:
            return "UNKNOWN"
        code = m.group(1).upper()

        if code in ("OK", "SUCCESS"):
            return "OK"
        if code in ("E", "ERROR"):
            return "ERROR"
        if code in ("W", "WARNING"):
            return "WARNING"
        
        return "UNKNOWN"