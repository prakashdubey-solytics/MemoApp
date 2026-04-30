from playwright.sync_api import Page
from utils import delete_post, wait_for_toast, unique_text

class TestDeletePost:
    def test_delete_post_shows_success_toast(self, page: Page, base_url: str):
        delete_post(page, base_url, unique_text("Post to Delete"))
        wait_for_toast(page, "Post deleted successfully!")

    def test_deleted_post_disappears_from_list(self, page: Page, base_url: str):
        # Implementation for checking post disappears
        pass
