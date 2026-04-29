from playwright.sync_api import Page
from utils import create_post, wait_for_toast, unique_text
import time

class TestToastBehaviour:
    def test_toast_disappears_after_timeout(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("Toast Timeout"), "Body")
        wait_for_toast(page, "Post created successfully!")
        time.sleep(5)
        assert not page.locator(".toast").is_visible()

    def test_toast_dismissed_on_click(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("Toast Click"), "Body")
        wait_for_toast(page, "Post created successfully!")
        page.click(".toast")
        assert not page.locator(".toast").is_visible()
