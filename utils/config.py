"""
config.py  –  Centralised configuration loader.
Reads from .env (or CI-injected environment variables).
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application
    BASE_URL: str = os.getenv("BASE_URL", "https://rahulshettyacademy.com")

    # Browser
    BROWSER: str = os.getenv("BROWSER", "chromium")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))

    # Credentials
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER: str = os.getenv("LOCKED_USER", "locked_out_user")
    TEST_PASSWORD: str = os.getenv("TEST_PASSWORD", "secret_sauce")

    # Reporting
    ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")

    # AI / Self-healing
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    SELF_HEALING_ENABLED: bool = os.getenv("SELF_HEALING_ENABLED", "true").lower() == "true"
    SELF_HEALING_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("SELF_HEALING_CONFIDENCE_THRESHOLD", "0.8")
    )
