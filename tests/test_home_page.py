from playwright.sync_api import Page

class TestHomePage:
    def test_page_loads(self, page: Page, base_url: str):
        page.goto(base_url)
        # assert page loaded
    def test_create_form_is_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        # assert create form is visible
