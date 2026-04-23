import os
import pytest


@pytest.fixture(scope="session")
def base_url():
    """Run Playwright against an already running app server."""
    return os.getenv("E2E_BASE_URL", "http://127.0.0.1:5000/")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Add ngrok header required to bypass the warning interstitial page."""
    headers = dict(browser_context_args.get("extra_http_headers", {}))
    headers["ngrok-skip-browser-warning"] = "true"
    return {
        **browser_context_args,
        "extra_http_headers": headers,
    }
