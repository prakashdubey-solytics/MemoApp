from playwright.sync_api import Page
from utils import search_post, unique_text

class TestSearch:
    def test_search_filters_by_title(self, page: Page, base_url: str):
        # Implementation for search by title
        pass

    def test_search_filters_posts(self, page: Page, base_url: str):
        # Implementation for search filters posts
        pass

    def test_search_no_results_shows_empty_state(self, page: Page, base_url: str):
        # Implementation for empty state
        pass
