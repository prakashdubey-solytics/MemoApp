from playwright.sync_api import Page
from utils import create_post, wait_for_toast, unique_text

class TestCreatePost:
    def test_create_post_shows_success_toast(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("My First Post"), "Hello Playwright!")
        wait_for_toast(page, "Post created successfully!")
