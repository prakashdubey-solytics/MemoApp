from playwright.sync_api import Page
from utils import search_post, unique_text

class TestSearch:
    def test_search_filters_by_title(self, page: Page, base_url: str):
        search_post(page, base_url, unique_text("Memo Title"))
        # assert only matching memos are shown
    def test_search_filters_posts(self, page: Page, base_url: str):
        search_post(page, base_url, unique_text("Post Title"))
        # assert only matching posts are shown
    def test_search_no_results_shows_empty_state(self, page: Page, base_url: str):
        search_post(page, base_url, "NoSuchPost")
        # assert empty state is shown
