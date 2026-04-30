from playwright.sync_api import Page
from utils import create_post, wait_for_toast, unique_text

class TestCreatePost:
    def test_create_post_shows_success_toast(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("My First Post"), "Hello Playwright!")
        wait_for_toast(page, "Post created successfully!")

class TestValidation:
    def test_create_post_empty_title_shows_error(self, page: Page, base_url: str):
        create_post(page, base_url, "", "Body")
        wait_for_toast(page, "Title is required!")
    def test_create_post_title_max_length(self, page: Page, base_url: str):
        long_title = 'A' * 101
        create_post(page, base_url, long_title, "Body")
        wait_for_toast(page, "Title must be at most 100 characters!")
