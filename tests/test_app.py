class TestHomePage:
    def test_create_post_validation_and_success_toast(self, page: Page, base_url: str):
        # Try to submit with empty fields
        page.goto(base_url)
        page.get_by_role("button", name="Create Post").click()
        wait_for_toast(page, "required")
        # Now submit valid post
        title = unique_text("Valid Post")
        body = "This is a valid post body"
        create_post(page, base_url, title, body)
        wait_for_toast(page, "Post created successfully!")

    def test_create_post_empty_title_shows_error_toast(self, page: Page, base_url: str):
        page.goto(base_url)
        page.fill("#body", "Body without title")
        page.get_by_role("button", name="Create Post").click()
        wait_for_toast(page, "required")

    def test_create_post_empty_body_shows_error_toast(self, page: Page, base_url: str):
        page.goto(base_url)
        page.fill("#title", unique_text("NoBody"))
        page.get_by_role("button", name="Create Post").click()
        wait_for_toast(page, "required")
