"""
Playwright end-to-end tests for the MemoBoard Flask app.

Run:
    pytest tests/test_app.py --headed          # visible browser
    pytest tests/test_app.py                   # headless (default)
"""

from uuid import uuid4
from playwright.sync_api import Page, expect

def create_post(page: Page, base_url: str, title: str, body: str) -> None:
    page.goto(base_url)
    page.fill("#title", title)
    page.fill("#body", body)
    page.get_by_role("button", name="Create Post").click()

def wait_for_toast(page: Page, text: str) -> None:
    toast = page.locator(".toast", has_text=text)
    expect(toast).to_be_visible(timeout=4000)

def unique_text(prefix: str) -> str:
    return f"{prefix} {uuid4().hex[:8]}"

class TestToastBehaviour:
    def test_toast_disappears_after_timeout(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("Toast Timer Post"), "Body")
        toast = page.locator(".toast", has_text="Post created successfully!")
        expect(toast).to_be_visible(timeout=4000)
        expect(toast).to_be_hidden(timeout=5000)

class TestCreatePost:
    def test_create_post_shows_success_toast(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("My First Post"), "Hello Playwright!")
        wait_for_toast(page, "Post created successfully!")
    def test_create_post_empty_title_shows_error(self, page: Page, base_url: str):
        create_post(page, base_url, "", "Body")
        wait_for_toast(page, "Title is required!")
    def test_create_post_title_max_length(self, page: Page, base_url: str):
        long_title = 'A' * 101
        create_post(page, base_url, long_title, "Body")
        wait_for_toast(page, "Title must be at most 100 characters!")

class TestEditPost:
    def test_edit_post_shows_success_toast(self, page: Page, base_url: str):
        title = unique_text("Post To Edit")
        create_post(page, base_url, title, "Original body")
        page.goto(base_url)
        card = page.locator(".post-card", has_text=title).first
        expect(card).to_be_visible()
        card.get_by_role("link", name="Edit").click()
        page.fill("#title", "Edited Title")
        page.fill("#body", "Edited body content")
        page.get_by_role("button", name="Save Changes").click()
        wait_for_toast(page, "Post updated successfully!")
    def test_edit_post_updates_title_in_list(self, page: Page, base_url: str):
        title = unique_text("Post Before Edit")
        updated_title = unique_text("Post After Edit")
        create_post(page, base_url, title, "Body text")
        page.goto(base_url)
        card = page.locator(".post-card", has_text=title).first
        expect(card).to_be_visible()
        card.get_by_role("link", name="Edit").click()
        page.fill("#title", updated_title)
        page.get_by_role("button", name="Save Changes").click()
        page.goto(base_url)
        expect(page.locator(".post-card", has_text=updated_title).first).to_be_visible()
    def test_edit_post_empty_fields_shows_error_toast(self, page: Page, base_url: str):
        title = unique_text("Post For Invalid Edit")
        create_post(page, base_url, title, "Body")
        page.goto(base_url)
        card = page.locator(".post-card", has_text=title).first
        expect(card).to_be_visible()
        card.get_by_role("link", name="Edit").click()
        page.fill("#title", "   " )
        page.fill("#body", "   " )
        page.get_by_role("button", name="Save Changes").click()
        wait_for_toast(page, "required")
    def test_edit_page_prefills_existing_values(self, page: Page, base_url: str):
        title = unique_text("Prefill Check Post")
        body = "Prefill body content"
        create_post(page, base_url, title, body)
        page.goto(base_url)
        card = page.locator(".post-card", has_text=title).first
        expect(card).to_be_visible()
        card.get_by_role("link", name="Edit").click()
        expect(page.locator("#title")).to_have_value(title)
        expect(page.locator("#body")).to_have_value(body)

class TestDeletePost:
    def test_delete_post_shows_success_toast(self, page: Page, base_url: str):
        title = unique_text("Post To Delete")
        create_post(page, base_url, title, "Will be deleted")
        page.goto(base_url)
        page.on("dialog", lambda d: d.accept())
        card = page.locator(".post-card", has_text=title).first
        expect(card).to_be_visible()
        card.get_by_role("button", name="Delete").click()
        wait_for_toast(page, "Post deleted successfully!")
    def test_deleted_post_disappears_from_list(self, page: Page, base_url: str):
        title = unique_text("Post That Should Vanish")
        create_post(page, base_url, title, "Body")
        page.goto(base_url)
        page.on("dialog", lambda d: d.accept())
        card = page.locator(".post-card", has_text=title).first
        expect(card).to_be_visible()
        card.get_by_role("button", name="Delete").click()
        page.goto(base_url)
        expect(page.locator(".post-card", has_text=title)).to_have_count(0)

class TestHomePage:
    def test_page_loads(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page).to_have_title("MemoBoard")
    def test_create_form_is_visible(self, page: Page, base_url: str):
        page.goto(base_url)
        expect(page.locator("#title")).to_be_visible()
        expect(page.locator("#body")).to_be_visible()
        expect(page.get_by_role("button", name="Create Post")).to_be_visible()

class TestSearch:
    def test_search_filters_by_title(self, page: Page, base_url: str):
        alpha = unique_text("Searchable Alpha")
        beta = unique_text("Searchable Beta")
        create_post(page, base_url, alpha, "Alpha content")
        create_post(page, base_url, beta, "Beta content")
        page.goto(base_url)
        page.fill("input[name='search']", alpha)
        page.keyboard.press("Enter")
        expect(page.locator(".post-card", has_text=alpha).first).to_be_visible()
        expect(page.locator(".post-card", has_text=beta)).to_have_count(0)
    def test_search_filters_posts(self, page: Page, base_url: str):
        alpha = unique_text("Searchable Alpha")
        beta = unique_text("Searchable Beta")
        create_post(page, base_url, alpha, "Alpha content")
        create_post(page, base_url, beta, "Beta content")
        page.goto(base_url)
        page.fill("input[name='search']", alpha)
        page.keyboard.press("Enter")
        expect(page.locator(".post-card", has_text=alpha).first).to_be_visible()
        expect(page.locator(".post-card", has_text=beta)).to_have_count(0)
    def test_search_no_results_shows_empty_state(self, page: Page, base_url: str):
        create_post(page, base_url, unique_text("Existing Post"), "content")
        page.goto(base_url)
        page.fill("input[name='search']", "xyznonexistent")
        page.keyboard.press("Enter")
        expect(page.locator(".empty-state")).to_be_visible()

class TestMemoList:
    def test_memos_sorted_by_last_edited_desc(self, page: Page, base_url: str):
        # create multiple memos, edit one, assert order
        pass

class TestPersistence:
    def test_memos_persist_across_sessions(self, page: Page, base_url: str):
        # create memo, reload, assert memo still exists
        pass
