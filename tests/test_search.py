from playwright.sync_api import Page
from utils import create_post, unique_text

class TestSearch:
    def test_search_filters_posts(self, page: Page, base_url: str):
        title = unique_text("Search Filter")
        create_post(page, base_url, title, "Body")
        page.fill("input[placeholder=Search]", title)
        assert page.locator(f"text={title}").is_visible()

    def test_search_no_results_shows_empty_state(self, page: Page, base_url: str):
        page.fill("input[placeholder=Search]", "NoSuchPost")
        assert page.locator("text=No posts found").is_visible()
