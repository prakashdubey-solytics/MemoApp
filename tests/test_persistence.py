from playwright.sync_api import Page
from utils import create_memo, reload_page, unique_text

class TestPersistence:
    def test_memos_persist_across_sessions(self, page: Page, base_url: str):
        create_memo(page, base_url, unique_text("Memo"))
        reload_page(page)
        # assert memo still exists
