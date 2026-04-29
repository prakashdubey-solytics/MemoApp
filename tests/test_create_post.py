from playwright.sync_api import Page
from utils import create_post, wait_for_toast, unique_text

class TestCreatePost:
    def test_create_post_shows_success_toast(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("My First Post"), "Hello Playwright!")
        wait_for_toast(page, "Post created successfully!")

    def test_created_post_appears_in_list(self, page: Page, base_url: str):
        title = unique_text("Post in List")
        create_post(page, base_url, title, "Body")
        page.goto(base_url)
        assert page.locator(f"text={title}").is_visible()

    def test_create_post_empty_title_shows_error_toast(self, page: Page, base_url: str):
        create_post(page, base_url, "", "Body")
        wait_for_toast(page, "Title is required")

    def test_create_post_empty_body_shows_error_toast(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("No Body"), "")
        wait_for_toast(page, "Body is required")
