from playwright.sync_api import Page
from utils import create_post, delete_post, wait_for_toast, unique_text

class TestDeletePost:
    def test_delete_post_shows_success_toast(self, page: Page, base_url: str):
        title = unique_text("Delete Toast")
        create_post(page, base_url, title, "Body")
        delete_post(page, base_url, title)
        wait_for_toast(page, "Post deleted successfully!")

    def test_deleted_post_disappears_from_list(self, page: Page, base_url: str):
        title = unique_text("Delete Disappear")
        create_post(page, base_url, title, "Body")
        delete_post(page, base_url, title)
        page.goto(base_url)
        assert not page.locator(f"text={title}").is_visible()
