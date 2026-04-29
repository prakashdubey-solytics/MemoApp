from playwright.sync_api import Page

class TestHomePage:
    def test_page_loads(self, page: Page, base_url: str):
        page.goto(base_url)
        assert page.title() == "Home"

    def test_create_form_is_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        assert page.locator("form#create-post").is_visible()
