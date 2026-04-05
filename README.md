# AI-Driven Playwright Python Framework

A production-grade test automation framework combining **Playwright + pytest + POM + Allure + Excel DDT + AI self-healing locators + MCP + GitHub Actions CI**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Browser Automation | Playwright (Python) |
| Test Runner | pytest + pytest-xdist |
| Design Pattern | Page Object Model (POM) |
| Reporting | Allure |
| Data-Driven Testing | Excel (openpyxl) |
| Logging | Python `logging` module |
| AI / Self-Healing | Anthropic Claude API |
| MCP Integration | MCP server (FastMCP) |
| CI/CD | GitHub Actions |
| Application Under Test | (https://rahulshettyacademy.com/) |

---

## Project Structure

```
ai_playwright_framework/
├── ai_core/
│   ├── self_healing.py        # AI-driven self-healing locator engine
│   └── ai_test_helper.py      # AI test data generation + failure analysis
├── config/
│   └── config.py              # Centralised config from .env
├── mcp_config/
│   ├── mcp_server.py          # MCP server exposing framework tools to Claude Desktop
│   └── claude_desktop_mcp.json# Claude Desktop MCP config template
├── pages/
│   ├── base_page.py           # BasePage wrapping all Playwright methods
│   ├── login_page.py          # Login POM
│   ├── inventory_page.py      # Inventory/Products POM
│   ├── cart_page.py           # Cart POM
│   └── checkout_page.py       # Checkout POM
├── tests/
│   ├── test_login.py          # Login tests (smoke + regression + DDT)
│   ├── test_inventory.py      # Inventory tests
│   ├── test_checkout.py       # Checkout E2E + DDT + AI data
│   └── test_self_healing.py   # Self-healing locator demo
├── test_data/
│   ├── login_data.xlsx        # DDT data for login
│   └── checkout_data.xlsx     # DDT data for checkout
├── utils/
│   ├── logger.py              # Centralised logging setup
│   └── excel_reader.py        # Excel DDT reader
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions CI pipeline
├── conftest.py                # Root pytest fixtures
├── pytest.ini                 # pytest configuration
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
└── .gitignore
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/ai-playwright-framework.git
cd ai-playwright-framework
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run tests

```bash
# Smoke tests only
pytest -m smoke -v

# Full regression suite
pytest -m regression -v

# Parallel execution (4 workers)
pytest -n 4 -v

# With Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## AI Features

### Self-Healing Locators

When a locator fails, `BasePage._locate()` automatically:
1. Captures current page HTML
2. Sends broken locator + HTML to Claude API
3. Claude returns the corrected locator + confidence score
4. Framework retries with the healed locator
5. All healing events are logged and attached to the Allure report

Enable/disable via `.env`:
```
SELF_HEALING_ENABLED=true
SELF_HEALING_CONFIDENCE_THRESHOLD=0.8
```

### AI Test Data Generation

```python
data = ai_helper.generate_test_data(
    "checkout form with first_name, last_name, postal_code for a customer in Hyderabad"
)
# Returns: {"first_name": "Arjun", "last_name": "Reddy", "postal_code": "500032"}
```

### AI Failure Analysis

```python
analysis = ai_helper.analyze_failure(
    error_message="TimeoutError: Waiting for selector",
    step_description="Clicking checkout button"
)
```

---

## MCP Integration (Claude Desktop)

The framework exposes an MCP server so you can control your test suite directly from Claude Desktop chat.

### Available MCP Tools

| Tool | Description |
|---|---|
| `run_test_suite` | Trigger pytest with optional marker filter |
| `get_healing_log` | Fetch self-healing history |
| `generate_test_data` | AI-generate test payloads |
| `analyze_test_failure` | Root-cause analysis for failures |

### Setup

1. Start the MCP server: `python mcp_config/mcp_server.py`
2. Copy `mcp_config/claude_desktop_mcp.json` content into your Claude Desktop config
3. In Claude Desktop, you can now say: *"Run the smoke tests"* or *"Show me the self-healing log"*

---

## CI/CD (GitHub Actions)

The pipeline triggers on:
- Every push to `main`
- Every **merged** pull request into `main`

Pipeline steps:
1. Setup Python 3.11
2. Install dependencies + Playwright browsers
3. Run **smoke tests** (must pass)
4. Run **regression tests** (allowed to continue on failure)
5. Upload Allure results as artifact
6. Publish Allure HTML report to **GitHub Pages**

### Required GitHub Secrets / Variables

| Name | Type | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Secret | Your Anthropic API key |
| `BASE_URL` | Variable | App URL (default: saucedemo.com) |

---

## Markers

| Marker | Description |
|---|---|
| `smoke` | Critical happy-path tests |
| `regression` | Full regression suite |
| `login` | Login-related tests |
| `cart` | Cart-related tests |
