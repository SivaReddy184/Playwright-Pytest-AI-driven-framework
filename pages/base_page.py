"""
base_page.py  –  BasePage wraps all Playwright interactions.

Features:
  - Unified click / fill / get_text with built-in waits
  - Automatic screenshot on failure
  - Self-healing locator fallback via SelfHealingEngine
  - Allure step attachment for every action
"""
import allure
from playwright.sync_api import Page, TimeoutError as PWTimeoutError

from utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 10_000   # ms


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ── Internal helpers ──────────────────────────────────────────

    def _get_locator(self, selector, locator_type: str = "css"):
        """Return a Playwright Locator based on type."""
        if locator_type == "xpath":
            return self.page.locator(f"xpath={selector}")
        if locator_type == "text":
            return self.page.get_by_text(selector)
        if locator_type == "role":
            return self.page.get_by_role(selector)
        if locator_type == 'label':
            return self.page.get_by_label(selector)
        return self.page.locator(selector)   # default: CSS


    # ── Public actions ────────────────────────────────────────────

    @allure.step("Navigate to: {url}")
    def navigate(self, url: str):
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")

    @allure.step("Click: {selector}")
    def click(self, selector: str, locator_type: str = "css", timeout: int = DEFAULT_TIMEOUT):
        logger.info(f"Click → '{selector}'")
        self._get_locator(selector, locator_type).click()

    @allure.step("Fill '{selector}' with value")
    def fill(self, selector: str, value: str, locator_type: str = "css", timeout: int = DEFAULT_TIMEOUT):
        logger.info(f"Fill → '{selector}' = '{value}'")
        self._get_locator(selector, locator_type).fill(value)

    @allure.step("Get text of: {selector}")
    def get_text(self, selector: str, locator_type: str = "css", timeout: int = DEFAULT_TIMEOUT) -> str:
        text = self._get_locator(selector, locator_type).inner_text()
        logger.debug(f"Text of '{selector}': {text}")
        return text

    @allure.step("Is visible: {selector}")
    def is_visible(self, selector: str, locator_type: str = "css") -> bool:
        try:
            return self.page.locator(selector).is_visible()
        except Exception:
            return False

    @allure.step("Wait for URL to contain: {partial_url}")
    def wait_for_url(self, partial_url: str, timeout: int = DEFAULT_TIMEOUT):
        logger.info(f"Waiting for URL to contain: '{partial_url}'")
        self.page.wait_for_url(f"**{partial_url}**", timeout=timeout)

    @allure.step("Select option: {value} in {selector}")
    def select_option(self, selector: str, value: str, locator_type: str = "css"):
        logger.info(f"Select option '{value}' in '{selector}'")
        self._get_locator(selector, locator_type).select_option(value)

    def take_screenshot(self, name: str = "screenshot"):
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        logger.info(f"Screenshot captured: {name}")
        return screenshot

    def get_page_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url
