"""
conftest.py  –  Root-level pytest fixtures.

Provides:
  - browser_context  : one Playwright BrowserContext per test (session or function scope)
  - page             : one Page per test, with auto-screenshot on failure
  - login_page / inventory_page / cart_page / checkout_page  : POM instances
  - ai_helper        : AITestHelper singleton
"""
import os
import pytest
import allure

from playwright.sync_api import sync_playwright, BrowserContext, Page

from pages.login_page import LoginPage
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

os.makedirs(Config.ALLURE_RESULTS_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# ── Playwright lifecycle ──────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browsers = {
        "chromium": playwright_instance.chromium,
        "firefox":  playwright_instance.firefox,
        "webkit":   playwright_instance.webkit,
    }
    browser_type = browsers.get(Config.BROWSER, playwright_instance.chromium) #chromium is default
    br = browser_type.launch(headless=Config.HEADLESS, slow_mo=Config.SLOW_MO)
    logger.info(f"Browser launched: {Config.BROWSER} | headless={Config.HEADLESS}")
    yield br
    br.close()

@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 768},
        record_video_dir="reports/videos/" if not Config.HEADLESS else None,
    )
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context, request):
    pg = context.new_page()
    yield pg
    # Auto-screenshot on test failure
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot = pg.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name=f"FAILURE_{request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )
        logger.warning(f"Failure screenshot captured for: {request.node.name}")
    pg.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to the page fixture via request.node.rep_call."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ── POM fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(page):
    return LoginPage(page)


# @pytest.fixture
# def inventory_page(page) -> InventoryPage:
#     return InventoryPage(page)
#
#
# @pytest.fixture
# def cart_page(page) -> CartPage:
#     return CartPage(page)
#
#
# @pytest.fixture
# def checkout_page(page) -> CheckoutPage:
#     return CheckoutPage(page)


@pytest.fixture
def logged_in_page(login_page, page):
    """Fixture that opens the app already logged in. Returns (page, inventory_page)."""
    login_page.open(Config.BASE_URL)
    login_page.login(Config.STANDARD_USER, Config.TEST_PASSWORD)
    return page, InventoryPage(page)
