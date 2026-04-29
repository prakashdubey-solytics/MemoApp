from playwright.sync_api import Page
from utils import create_post, edit_post, wait_for_toast, unique_text

class TestEditPost:
    def test_edit_post_shows_success_toast(self, page: Page, base_url: str):
        title = unique_text("Edit Toast")
        create_post(page, base_url, title, "Body")
        edit_post(page, base_url, title, "Edited Title", "Edited Body")
        wait_for_toast(page, "Post updated successfully!")

    def test_edit_post_updates_title_in_list(self, page: Page, base_url: str):
        title = unique_text("Edit Title")
        create_post(page, base_url, title, "Body")
        edit_post(page, base_url, title, "New Title", "Body")
        page.goto(base_url)
        assert page.locator(f"text=New Title").is_visible()

    def test_edit_post_empty_fields_shows_error_toast(self, page: Page, base_url: str):
        title = unique_text("Edit Empty")
        create_post(page, base_url, title, "Body")
        edit_post(page, base_url, title, "", "")
        wait_for_toast(page, "Title and body are required")

    def test_edit_page_prefills_existing_values(self, page: Page, base_url: str):
        title = unique_text("Prefill")
        body = "Prefill Body"
        create_post(page, base_url, title, body)
        page.goto(f"{base_url}/edit/{title}")
        assert page.locator("input[name=title]").input_value() == title
        assert page.locator("textarea[name=body]").input_value() == body
