import pytest
import time

from src.pages.components.statusbar_component import StatusbarComponent
from src.pages.components.toolbar_component import ToolbarComponent

def test_toolbar_actions_smoke(app):
    toolbar = app.toolbar
    statusbar = app.statusbar

    time.sleep(5)
    toolbar.enter_command("mb1c")
    # time.sleep(5)
    msg = statusbar.get()
    assert msg.type != "ERROR", f"Error tras OK Code: {msg.text}"

    
    toolbar.back()
    msg = statusbar.get()
    assert msg.type != "ERROR", f"Error tras Back: {msg.text}"
