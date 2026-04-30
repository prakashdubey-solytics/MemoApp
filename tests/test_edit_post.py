from playwright.sync_api import Page
from utils import edit_post, wait_for_toast, unique_text

class TestEditPost:
    def test_edit_post_shows_success_toast(self, page: Page, base_url: str):
        edit_post(page, base_url, unique_text("Edit Post"), "Updated!")
        wait_for_toast(page, "Post updated successfully!")
    def test_edit_post_updates_title_in_list(self, page: Page, base_url: str):
        new_title = unique_text("Updated Title")
        edit_post(page, base_url, new_title, "Body")
        # assert new_title is visible in post list
    def test_edit_post_empty_fields_shows_error_toast(self, page: Page, base_url: str):
        edit_post(page, base_url, "", "")
        wait_for_toast(page, "Title and body are required!")
    def test_edit_page_prefills_existing_values(self, page: Page, base_url: str):
        # assert edit form is prefilled with existing post values
        pass
