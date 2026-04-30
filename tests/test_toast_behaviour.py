from playwright.sync_api import Page
from utils import wait_for_toast

class TestToastBehaviour:
    def test_toast_disappears_after_timeout(self, page: Page, base_url: str):
        # trigger toast, wait, assert toast disappears
        pass
    def test_toast_dismissed_on_click(self, page: Page, base_url: str):
        # trigger toast, click, assert toast disappears
        pass
