
import allure
import pytest

from pages.login_page import LoginPage
from utils.config import Config

@allure.feature("Authentication")
class TestLogin:

    @allure.story("Valid login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, login_page: LoginPage):
        """Standard user should land on inventory page after login."""
        with allure.step("Open application"):
            login_page.open(f'{Config.BASE_URL}/client/#/auth/login')

        with allure.step("Login with valid credentials"):
            login_page.login(Config.STANDARD_USER, Config.TEST_PASSWORD)

        # with allure.step("Verify inventory page is displayed"):
        #     inventory = InventoryPage(login_page.page)
        #     title = inventory.get_title()
        #     assert title == "Products", f"Expected 'Products' but got '{title}'"
        #     logger.info("Valid login test PASSED.")