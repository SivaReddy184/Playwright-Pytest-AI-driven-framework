import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage(BasePage):

    USERNAME_INPUT = '#userEmail'
    PASSWORD_INPUT = '#userPassword'
    LOGIN_BUTTON = '#login'
    ERROR_MESSAGE = '#toast-container'

    def __init__(self, page):
        super().__init__(page)

    @allure.step("Open Login Page")
    def open(self, base_url):
        self.navigate(base_url)
        logger.info("Login page opened")

    @allure.step("Login with username='{username}'")
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        logger.info(f"Logged in with {username}")

