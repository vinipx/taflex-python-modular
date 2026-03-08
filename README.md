# 🚀 taflex-py

[![CI](https://github.com/vinipx/taflex-python-modular/actions/workflows/ci.yml/badge.svg)](https://github.com/vinipx/taflex-python-modular/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A modular, enterprise-grade Python test automation framework designed for high-performance API, Web, and Mobile testing. 

## 🏗️ Modular Architecture

`taflex-py` utilizes **Namespace Packages** and **Dynamic Lazy Loading**. This allows teams to maintain a lightweight environment by installing only what they need while inheriting a robust core for logging, reporting, and configuration.

### Framework Structure
- **`taflex.core`**: Shared logic, drivers (ABCs), and enterprise utilities.
- **`taflex.api`**: High-speed API testing using `httpx`.
- **`taflex.web`**: Modern web automation powered by `playwright`.
- **`taflex.mobile`**: Cross-platform mobile testing via `appium`.
- **`taflex.contract`**: Consumer-driven contract testing with `pact`.

---

## 🛠️ Installation & Setup

We provide an initialization script for developers working on the framework and a project scaffolding wizard for creating new projects.

### Framework Initialization (For Developers)
If you've cloned this repository to work on the framework itself or run the existing tests:
```bash
chmod +x init.sh
./init.sh
source .venv/bin/activate
```
This script creates a virtual environment, installs all dependencies in editable mode, and sets up Playwright.

### Quickstart Wizard (For New Projects)
To generate a new test automation project using `taflex-py` as a template:
```bash
chmod +x setup.sh
./setup.sh
```

The wizard will guide you through:
1. **Module Selection**: Web (Playwright), API (HTTPX), Mobile (Appium), or Contract (Pact).
2. **Reporting**: Allure, ReportPortal, Jira Xray, or HTML.
3. **CI/CD**: Automatic generation of GitHub Actions or GitLab CI workflows.
4. **Environment**: Automatic `.env` and `pyproject.toml` generation.

---

## ⚙️ Configuration

The framework uses `pydantic-settings` for robust environment management. Create a `.env` file in your root directory:

| Variable | Description | Default |
|----------|-------------|---------|
| `EXECUTION_MODE` | `web`, `api`, or `mobile` | `web` |
| `BROWSER` | `chromium`, `firefox`, `webkit` | `chromium` |
| `HEADLESS` | Run browser without UI (`true`/`false`) | `true` |
| `REPORTERS` | Comma-separated (e.g., `allure,xray,reportportal`) | `""` |
| `BASE_URL` | Application under test URL | `None` |

---

## 🚀 Usage

The framework exposes a unified `driver` fixture that automatically initializes the correct client based on your configuration or test markers.

### API Testing
```python
@pytest.mark.api
def test_get_user(driver):
    response = driver.get("/users/1")
    assert response.status_code == 200
```

### Web Testing
```python
@pytest.mark.web
def test_login(driver):
    page = driver.start() # Returns Playwright Page object
    page.goto("https://example.com")
    assert page.title() == "Example Domain"
```

---

## 📊 Integrations

`taflex-py` comes pre-configured with industry-standard reporting and management tools:

- **Allure Reports**: Rich interactive test reports.
- **EPAM ReportPortal**: AI-powered dashboard for test results.
- **Jira Xray**: Native integration for test management and requirement traceability.
- **Pact**: Contract testing for microservices.

---

## 🔄 CI/CD

The framework is optimized for CI/CD environments with built-in support for **GitHub Actions** and **GitLab CI**.

Run tests in CI with optimized flags:
```bash
pytest -n auto --dist loadscope --alluredir=reports/allure-results
```

---

## 🛡️ Engineering Standards
- **Linting**: Ruff (fastest Python linter).
- **Typing**: Mypy (static type checking).
- **Parallelism**: Pytest-xdist for distributed execution.
