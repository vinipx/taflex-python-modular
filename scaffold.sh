#!/bin/bash

echo "============================================"
echo "  taflex-py - Project Scaffolding Wizard"
echo "============================================"
echo "This script will generate a new test automation project"
echo "by copying the selected framework source code into your target directory."
echo ""

echo "Which testing modules do you need?"
echo "Answer 'y' (yes) or 'n' (no) for each option."
echo ""

modules=()
deps=("pytest" "pydantic" "pydantic-settings" "SQLAlchemy" "ruff" "mypy" "pytest-xdist" "radon" "pytest-cov")

read -p "1) Web Testing (Playwright)? [y/n]: " req_web
if [[ "$req_web" =~ ^[Yy]$ ]] || [[ -z "$req_web" ]]; then
    modules+=("web")
    deps+=("playwright")
fi

read -p "2) API Testing (HTTPX)? [y/n]: " req_api
if [[ "$req_api" =~ ^[Yy]$ ]] || [[ -z "$req_api" ]]; then
    modules+=("api")
    deps+=("httpx")
fi

read -p "3) Mobile Testing (Appium)? [y/n]: " req_mobile
if [[ "$req_mobile" =~ ^[Yy]$ ]] || [[ -z "$req_mobile" ]]; then
    modules+=("mobile")
    deps+=("Appium-Python-Client")
fi

read -p "4) Contract Testing (Pact)? [y/n]: " req_contract
if [[ "$req_contract" =~ ^[Yy]$ ]] || [[ -z "$req_contract" ]]; then
    modules+=("contract")
    deps+=("pact-python")
fi

read -p "5) BDD Testing (pytest-bdd)? [y/n]: " req_bdd
if [[ "$req_bdd" =~ ^[Yy]$ ]] || [[ -z "$req_bdd" ]]; then
    modules+=("bdd")
    deps+=("pytest-bdd")
fi

if [ ${#modules[@]} -eq 0 ]; then
    echo "No modules selected. Defaulting to 'web'."
    modules=("web")
    deps+=("playwright")
fi

# Join modules with comma for display
IFS=','
extras="${modules[*]}"
unset IFS

echo ""
echo "Which reporting tools do you need?"
echo "Answer 'y' (yes) or 'n' (no) for each option."
echo ""

reports=()
pytest_addopts="-v --tb=short"

read -p "1) HTML Report (pytest-html)? [y/n]: " req_html
if [[ "$req_html" =~ ^[Yy]$ ]] || [[ -z "$req_html" ]]; then
    reports+=("html")
    deps+=("pytest-html")
    pytest_addopts="$pytest_addopts --html=reports/report.html"
fi

read -p "2) Allure Report? [y/n]: " req_allure
if [[ "$req_allure" =~ ^[Yy]$ ]] || [[ -z "$req_allure" ]]; then
    reports+=("allure")
    deps+=("allure-pytest")
    pytest_addopts="$pytest_addopts --alluredir=reports/allure-results"
fi

read -p "3) ReportPortal? [y/n]: " req_rp
if [[ "$req_rp" =~ ^[Yy]$ ]]; then
    reports+=("reportportal")
    deps+=("pytest-reportportal")
fi

read -p "4) Jira Xray? [y/n]: " req_xray
if [[ "$req_xray" =~ ^[Yy]$ ]]; then
    reports+=("xray")
    deps+=("pytest-jira-xray")
fi

echo ""
echo "Do you want to enable AI Agent (MCP) support?"
read -p "Model Context Protocol (MCP) Server [y/n]: " req_mcp
if [[ "$req_mcp" =~ ^[Yy]$ ]] || [[ -z "$req_mcp" ]]; then
    modules+=("mcp")
    deps+=("mcp>=1.0.0")
fi

echo ""
echo "Which CI/CD configuration do you need?"
echo "1) GitHub Actions"
echo "2) GitLab CI"
echo "3) None (to be set manually)"
read -p "Select CI type [1-3]: " ci_choice

case "$ci_choice" in
    1) ci_type="github" ;;
    2) ci_type="gitlab" ;;
    *) ci_type="none" ;;
esac

echo ""
read -p "Do you want to include Documentation (MkDocs)? [y/n]: " req_docs
if [[ "$req_docs" =~ ^[Yy]$ ]] || [[ -z "$req_docs" ]]; then
    req_docs="y"
else
    req_docs="n"
fi

echo ""
echo "Selected modules: $extras"
echo "Selected reports: ${reports[*]}"
echo ""

read -p "Enter the project directory path (default: ./my-test-project): " project_path
project_path=${project_path:-./my-test-project}

# Get absolute path of the framework template
TEMPLATE_DIR=$(pwd)

echo "Scaffolding project at $project_path..."

# Create project structure
mkdir -p "$project_path/tests/pages"
mkdir -p "$project_path/src/taflex"

# Generate .gitignore
cat <<EOF > "$project_path/.gitignore"
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script, before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Reports and artifacts
reports/
allure-results/

# Environments
.env
.venv
venv/
ENV/
env.bak
venv.bak

# IDEs
.idea/
.vscode/
*.swp
*.swo

# OS-specific
.DS_Store
EOF

# Copy the core module
cp -R "$TEMPLATE_DIR/src/taflex/core" "$project_path/src/taflex/"

# Copy codechecks.sh
if [ -f "$TEMPLATE_DIR/codechecks.sh" ]; then
    cp "$TEMPLATE_DIR/codechecks.sh" "$project_path/"
    chmod +x "$project_path/codechecks.sh"
fi

# Copy selected modules
for mod in "${modules[@]}"; do
    if [ -d "$TEMPLATE_DIR/src/taflex/$mod" ]; then
        cp -R "$TEMPLATE_DIR/src/taflex/$mod" "$project_path/src/taflex/"
    fi
done

# Copy overrides if it exists (for custom docs style)
if [ "$req_docs" == "y" ]; then
    if [ -d "$TEMPLATE_DIR/docs/overrides" ]; then
        mkdir -p "$project_path/docs"
        cp -R "$TEMPLATE_DIR/docs/overrides" "$project_path/docs/"
    fi
fi

# Handle CI/CD configuration
if [ "$ci_type" == "github" ]; then
    echo "Configuring GitHub Actions..."
    mkdir -p "$project_path/.github/workflows"
cat <<EOF > "$project_path/.github/workflows/ci.yml"
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build-and-validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .

    - name: Install Playwright Browsers
      run: playwright install --with-deps

    - name: Lint with Ruff
      run: ruff check .

    - name: Type check with Mypy
      run: mypy src/ tests/ || echo "Mypy checks failed but continuing..."

    - name: Run Framework Tests
      run: pytest

    - name: Run Architecture & Code Coverage Checks
      run: ./codechecks.sh
EOF

if [[ " ${reports[*]} " =~ " allure " ]]; then
    echo "Generating Allure reporting skeleton..."
cat <<EOF > "$project_path/.github/workflows/allure.yml"
name: Allure Report

on:
  workflow_run:
    workflows: ["CI"] # Change this to your test workflow name
    types: [completed]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  generate-report:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch' || github.event.workflow_run.conclusion == 'success'
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Download test results
        # This is a skeleton. You'll need to upload artifacts in your test workflow first.
        uses: actions/download-artifact@v4
        with:
          name: allure-results
          path: reports/allure-results
        continue-on-error: true

      - name: Generate Allure Report
        uses: simple-elf/allure-report-action@master
        if: always()
        with:
          allure_results: reports/allure-results
          allure_history: allure-history
          keep_reports: 20

      - name: Deploy report to Github Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: \${{ secrets.GITHUB_TOKEN }}
          publish_dir: allure-history
          destination_dir: allure-report
          keep_files: true
EOF
fi

    # Also copy the docs workflow if it exists
    if [ "$req_docs" == "y" ]; then
        if [ -f "$TEMPLATE_DIR/.github/workflows/docs.yml" ]; then
            cp "$TEMPLATE_DIR/.github/workflows/docs.yml" "$project_path/.github/workflows/"
        fi
    fi
elif [ "$ci_type" == "gitlab" ]; then
    echo "Configuring GitLab CI..."
cat <<EOF > "$project_path/.gitlab-ci.yml"
image: python:3.10

stages:
  - build
  - lint
  - test
  - report
  - deploy

variables:
  PIP_CACHE_DIR: "\$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - python -m pip install --upgrade pip
  - pip install -e .
  - playwright install --with-deps

lint:
  stage: lint
  script:
    - ruff check .
    - mypy src/ tests/ || echo "Mypy checks failed but continuing..."
  rules:
    - if: '\$CI_PIPELINE_SOURCE == "push" || \$CI_PIPELINE_SOURCE == "merge_request_event"'

test:
  stage: test
  script:
    - pytest
    - ./codechecks.sh
  artifacts:
    when: always
    paths:
      - reports/
    expire_in: 1 week
  rules:
    - if: '\$CI_PIPELINE_SOURCE == "push" || \$CI_PIPELINE_SOURCE == "merge_request_event"'
EOF

if [[ " ${reports[*]} " =~ " allure " ]]; then
cat <<EOF >> "$project_path/.gitlab-ci.yml"

allure_report:
  stage: report
  image: node:18-alpine
  script:
    - npm install -g allure-commandline
    - allure generate reports/allure-results -o allure-report
  artifacts:
    paths:
      - allure-report
    expire_in: 1 day
  rules:
    - if: '\$CI_PIPELINE_SOURCE == "push" || \$CI_PIPELINE_SOURCE == "merge_request_event"'
EOF
fi

if [[ "$req_docs" == "y" ]] || [[ " ${reports[*]} " =~ " allure " ]]; then
cat <<EOF >> "$project_path/.gitlab-ci.yml"

pages:
  stage: deploy
  script:
EOF

if [ "$req_docs" == "y" ]; then
cat <<EOF >> "$project_path/.gitlab-ci.yml"
    - pip install mkdocs-material mkdocs-mermaid2-plugin
    - mkdocs build --site-dir public
EOF
else
cat <<EOF >> "$project_path/.gitlab-ci.yml"
    - mkdir -p public
EOF
fi

if [[ " ${reports[*]} " =~ " allure " ]]; then
cat <<EOF >> "$project_path/.gitlab-ci.yml"
    - mkdir -p public/allure-report
    - cp -R allure-report/* public/allure-report/
EOF
fi

cat <<EOF >> "$project_path/.gitlab-ci.yml"
  artifacts:
    paths:
      - public
  rules:
    - if: '\$CI_COMMIT_BRANCH == \$CI_DEFAULT_BRANCH'
EOF
fi
fi

# Generate pyproject.toml (Modern standard)
echo "Generating pyproject.toml..."

# Prepare dependencies strings for TOML
base_deps="\"pytest\", \"pydantic\", \"pydantic-settings\", \"SQLAlchemy\", \"ruff\", \"mypy\", \"pytest-xdist\", \"radon\", \"pytest-cov\""
for rep in "${reports[@]}"; do
    if [ "$rep" == "allure" ]; then base_deps="$base_deps, \"allure-pytest\""; fi
    if [ "$rep" == "reportportal" ]; then base_deps="$base_deps, \"pytest-reportportal\""; fi
    if [ "$rep" == "xray" ]; then base_deps="$base_deps, \"pytest-jira-xray\""; fi
done

cat <<EOF > "$project_path/pyproject.toml"
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "taflex-py-project"
version = "0.1.0"
description = "Modular test automation project scaffolded with taflex-py"
dependencies = [
    $base_deps
]

[project.optional-dependencies]
EOF

for mod in "${modules[@]}"; do
    if [ "$mod" == "web" ]; then echo "web = [\"playwright\"]" >> "$project_path/pyproject.toml"; fi
    if [ "$mod" == "api" ]; then echo "api = [\"httpx\"]" >> "$project_path/pyproject.toml"; fi
    if [ "$mod" == "mobile" ]; then echo "mobile = [\"Appium-Python-Client\"]" >> "$project_path/pyproject.toml"; fi
    if [ "$mod" == "contract" ]; then echo "contract = [\"pact-python\"]" >> "$project_path/pyproject.toml"; fi
    if [ "$mod" == "bdd" ]; then echo "bdd = [\"pytest-bdd\"]" >> "$project_path/pyproject.toml"; fi
    if [ "$mod" == "mcp" ]; then echo "mcp = [\"mcp>=1.0.0\"]" >> "$project_path/pyproject.toml"; fi
done
echo "all = [\"taflex-py-project[$(IFS=,; echo "${modules[*]}")]\"]" >> "$project_path/pyproject.toml"

if [[ " ${modules[*]} " =~ " mcp " ]]; then
cat <<EOF >> "$project_path/pyproject.toml"

[project.scripts]
taflex-mcp = "taflex.mcp_server:main"
EOF
fi

cat <<EOF >> "$project_path/pyproject.toml"

[tool.pytest.ini_options]
addopts = "$pytest_addopts"
testpaths = ["tests"]
pythonpath = ["src", "."]
filterwarnings = [
    "ignore::DeprecationWarning:pytest_reportportal.plugin",
]
markers = [
    "api: mark test as api test",
    "web: mark test as web test",
    "mobile: mark test as mobile test",
    "bdd: mark test as bdd test",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
EOF

# Determine the primary execution mode for the .env file
primary_mode=${modules[0]}

# Generate framework config file
cat <<EOF > "$project_path/.env"
# ==============================================================================
# TAFLEX PY - Environment Configuration
# ==============================================================================

# ------------------------------------------------------------------------------
# Core Execution Settings
# ------------------------------------------------------------------------------
# The primary mode of execution. 
# Supported values: web, api, mobile
EXECUTION_MODE=$primary_mode

# Global timeout for requests, element waiting, etc. (in milliseconds)
# Default: 30000
TIMEOUT=30000
EOF

if [[ " ${modules[*]} " =~ " web " ]]; then
cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# Web Automation Settings (Playwright)
# ------------------------------------------------------------------------------
# The browser engine to use.
# Supported values: chromium, firefox, webkit
BROWSER=chromium

# Whether to run the browser in headless mode (no UI).
# Supported values: true, false
HEADLESS=true

# The base URL for web navigation.
BASE_URL=https://the-internet.herokuapp.com
EOF
fi

if [[ " ${modules[*]} " =~ " api " ]]; then
cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# API Automation Settings
# ------------------------------------------------------------------------------
# The base URL for API requests.
API_BASE_URL=https://jsonplaceholder.typicode.com

# The underlying HTTP client to use for API testing.
# Supported values: playwright (hybrid flows), httpx (high-speed specialized)
API_PROVIDER=httpx
EOF
fi

if [[ " ${modules[*]} " =~ " mobile " ]]; then
cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# Mobile Automation Settings (Appium)
# ------------------------------------------------------------------------------
# The Appium server URL.
APPIUM_SERVER_URL=http://localhost:4723/wd/hub

# Target platform for mobile execution.
# Supported values: Android, iOS
PLATFORM_NAME=Android

# Specific device to target (Uncomment to use)
# DEVICE_NAME=emulator-5554
EOF
fi

cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# Cloud Grid Settings (BrowserStack / SauceLabs)
# ------------------------------------------------------------------------------
# Target execution platform.
# Supported values: local, browserstack, saucelabs
CLOUD_PLATFORM=local

# Cloud provider credentials. (Uncomment and populate if using cloud grid)
# CLOUD_USER=your_username
# CLOUD_KEY=your_access_key

# Specific environment requirements for cloud execution.
# BROWSER_VERSION=latest
# OS=Windows
# OS_VERSION=11
EOF

# Build a string for REPORTERS
IFS=','
reporters_str="${reports[*]}"
unset IFS

cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# Reporting & Integration Settings
# ------------------------------------------------------------------------------
# Comma-separated list of active reporters.
# Example: html, allure, reportportal, xray
REPORTERS=$reporters_str
EOF

if [[ " ${reports[*]} " =~ " allure " ]]; then
cat <<EOF >> "$project_path/.env"

# Directory to output Allure results.
ALLURE_RESULTS_DIR=allure-results
EOF
fi

if [[ " ${reports[*]} " =~ " reportportal " ]]; then
cat <<EOF >> "$project_path/.env"

# --- EPAM ReportPortal Integration ---
RP_ENDPOINT=https://rp.yourcompany.com/api/v1
RP_API_KEY=your_secret_api_key
RP_PROJECT=taflex-automation
RP_LAUNCH=nightly_build
# RP_DESCRIPTION=Regression Suite
# RP_ATTRIBUTES=env:dev;team:qa
EOF
else
cat <<EOF >> "$project_path/.env"

# --- EPAM ReportPortal Integration ---
# RP_ENDPOINT=https://rp.yourcompany.com/api/v1
# RP_API_KEY=your_secret_api_key
# RP_PROJECT=taflex-automation
# RP_LAUNCH=nightly_build
# RP_DESCRIPTION=Regression Suite
# RP_ATTRIBUTES=env:dev;team:qa
EOF
fi

if [[ " ${reports[*]} " =~ " xray " ]]; then
cat <<EOF >> "$project_path/.env"

# --- Jira Xray Integration ---
XRAY_ENABLED=true
XRAY_API_BASE_URL=https://xray.cloud.getxray.app
XRAY_CLIENT_ID=your_xray_client_id
XRAY_CLIENT_SECRET=your_xray_client_secret
# XRAY_PROJECT_KEY=PROJ
# XRAY_TEST_PLAN_KEY=PROJ-100
# XRAY_TEST_EXEC_KEY=PROJ-101
# XRAY_ENVIRONMENT=staging
EOF
else
cat <<EOF >> "$project_path/.env"

# --- Jira Xray Integration ---
XRAY_ENABLED=false
# XRAY_API_BASE_URL=https://xray.cloud.getxray.app
# XRAY_CLIENT_ID=your_xray_client_id
# XRAY_CLIENT_SECRET=your_xray_client_secret
# XRAY_PROJECT_KEY=PROJ
# XRAY_TEST_PLAN_KEY=PROJ-100
# XRAY_TEST_EXEC_KEY=PROJ-101
# XRAY_ENVIRONMENT=staging
EOF
fi

if [[ " ${modules[*]} " =~ " contract " ]]; then
cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# Pact Contract Testing Settings
# ------------------------------------------------------------------------------
PACT_ENABLED=true
PACT_CONSUMER=taflex-consumer
PACT_PROVIDER=taflex-provider
PACT_DIR=pacts
# PACT_BROKER_URL=https://your-pact-broker.com
# PACT_BROKER_TOKEN=your_broker_token
# PACT_LOG_LEVEL=info # debug, info, warn, error
EOF
else
cat <<EOF >> "$project_path/.env"

# ------------------------------------------------------------------------------
# Pact Contract Testing Settings
# ------------------------------------------------------------------------------
PACT_ENABLED=false
# PACT_CONSUMER=taflex-consumer
# PACT_PROVIDER=taflex-provider
# PACT_DIR=pacts
# PACT_BROKER_URL=https://your-pact-broker.com
# PACT_BROKER_TOKEN=your_broker_token
# PACT_LOG_LEVEL=info # debug, info, warn, error
EOF
fi

# Generate basic conftest.py
cat <<EOF > "$project_path/tests/conftest.py"
import pytest

# Import the core conftest to load global fixtures like 'driver'
pytest_plugins = [
    "taflex.core.conftest"
]

# You can add project-specific fixtures here.
EOF

# Generate sample Page Objects and tests for each selected module
for mod in "${modules[@]}"; do
    if [ "$mod" == "web" ]; then
cat <<EOF > "$project_path/tests/pages/search_page.py"
from taflex.core.drivers.base_page import BasePage

class SearchPage(BasePage):
    """Sample Page Object for Web testing."""
    URL = "https://www.google.com"
    SEARCH_INPUT = "[name='q']"
    
    def open(self):
        self.navigate_to(self.URL)
        return self

    def search_for(self, query):
        self.driver.type(self.SEARCH_INPUT, query)
        self.driver.page.keyboard.press("Enter")
        self.driver.page.wait_for_load_state("networkidle")
EOF

cat <<EOF > "$project_path/tests/test_sample_web.py"
import pytest
from tests.pages.search_page import SearchPage

@pytest.mark.web
def test_example_web_pom(driver):
    """Sample Web test using Page Object Model."""
    search_page = SearchPage(driver)
    search_page.open()
    search_page.search_for("taflex-py modular framework")
    
    assert "taflex-py" in driver.page.title() or "google" in driver.page.url
EOF
    elif [ "$mod" == "api" ]; then
cat <<EOF > "$project_path/tests/test_sample_api.py"
import pytest

@pytest.mark.api
def test_example_api(driver):
    print(f"Using: {driver.driver_type}")
    assert "HTTPX" in driver.driver_type
EOF
    elif [ "$mod" == "mobile" ]; then
cat <<EOF > "$project_path/tests/pages/app_page.py"
from taflex.core.drivers.base_page import BasePage

class AppPage(BasePage):
    """Sample Page Object for Mobile testing."""
    LOGIN_BUTTON = "login_button"
    
    def tap_login(self):
        self.driver.click(self.LOGIN_BUTTON)
EOF

cat <<EOF > "$project_path/tests/test_sample_mobile.py"
import pytest
import socket
from tests.pages.app_page import AppPage

def is_appium_running():
    try:
        # Check if something is listening on the default Appium port
        socket.create_connection(("127.0.0.1", 4723), timeout=1)
        return True
    except OSError:
        return False

@pytest.mark.mobile
@pytest.mark.skipif(not is_appium_running(), reason="Appium Server is not running on port 4723")
def test_example_mobile_pom(driver):
    """Sample Mobile test using Page Object Model."""
    app_page = AppPage(driver)
    print(f"Using: {driver.driver_type}")
    assert "Appium" in driver.driver_type
    
    # app_page.tap_login()
EOF
    elif [ "$mod" == "contract" ]; then
cat <<EOF > "$project_path/tests/test_sample_contract.py"
import pytest
import requests

def test_example_contract(pact):
    """
    Sample Contract test demonstrating Pact interaction.
    """
    expected_body = {"status": "up"}
    
    (pact
     .given("User service is healthy")
     .upon_receiving("a request for health check")
     .with_request("GET", "/health")
     .will_respond_with(200, body=expected_body))
    
    # In a real test, this would be your API client or service code
    # using pact.uri to connect to the mock service
    response = requests.get(f"{pact.uri}/health")
    
    assert response.status_code == 200
    assert response.json() == expected_body
    
    # Pact verification is handled by the fixture teardown
EOF
    elif [ "$mod" == "bdd" ]; then
mkdir -p "$project_path/tests/features"
cat <<EOF > "$project_path/tests/features/sample.feature"
Feature: Sample Feature
  Scenario: Sample Scenario
    Given I have a driver
    When I check the driver type
    Then It should be configured correctly
EOF

cat <<EOF > "$project_path/tests/test_sample_bdd.py"
import pytest
from pytest_bdd import scenario, given, when, then

@pytest.mark.bdd
@scenario('features/sample.feature', 'Sample Scenario')
def test_sample_bdd():
    pass

@given("I have a driver")
def have_driver(driver):
    assert driver is not None

@when("I check the driver type")
def check_driver_type(driver):
    print(f"Driver type: {driver.driver_type}")

@then("It should be configured correctly")
def configured_correctly():
    assert True
EOF
    fi
done


# ==============================================================================
# Generate Project Documentation
# ==============================================================================
if [ "$req_docs" == "y" ]; then
mkdir -p "$project_path/docs"

# Copy stylesheets if they exist
if [ -d "$TEMPLATE_DIR/docs/stylesheets" ]; then
    cp -R "$TEMPLATE_DIR/docs/stylesheets" "$project_path/docs/"
fi

cat <<EOF > "$project_path/docs/README.md"
# Project Documentation

Welcome to your generated TAFLEX PY Modular project.
This directory contains essential guides and tutorials tailored to your selected stack.

* [Core Framework Architecture](core-architecture.md)
EOF

cat <<EOF > "$project_path/docs/core-architecture.md"
# Core Framework Architecture

## Configuration (\`.env\`)
TAFLEX PY uses Pydantic to strictly validate configuration from your \`.env\` file via the \`AppConfig\` class.
When you run tests, \`conftest.py\` instantiates this config and passes it to the \`DriverFactory\`.

## DriverFactory and conftest.py
The core of the execution lies in the \`DriverFactory\`. Depending on the \`EXECUTION_MODE\` in your \`.env\` or the Pytest marker applied to your test (e.g., \`@pytest.mark.api\`), the Factory will spin up the correct client (\`PlaywrightDriver\`, \`HttpxClient\`, etc.) without you having to change your test logic.

To write a test, simply request the \`driver\` fixture:
\`\`\`python
def test_example(driver):
    pass
\`\`\`
EOF

for mod in "${modules[@]}"; do
    if [ "$mod" == "web" ]; then
cat <<EOF > "$project_path/docs/web-testing.md"
# Web Testing with Playwright

Web testing is powered by Playwright. The framework automatically handles browser contexts, page creation, and cleanup.

## Page Object Model
Use the \`BasePage\` to create your page objects.

\`\`\`python
from taflex.core.drivers.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://example.com/login"
    USERNAME_INPUT = "#username"
    
    def login(self, username):
        self.navigate_to(self.URL)
        self.driver.type(self.USERNAME_INPUT, username)
\`\`\`

## Running Tests
Run all web tests:
\`\`\`bash
pytest -m web
\`\`\`
EOF
        echo "* [Web Testing Guide](web-testing.md)" >> "$project_path/docs/README.md"
    elif [ "$mod" == "api" ]; then
cat <<EOF > "$project_path/docs/api-testing.md"
# API Testing with HTTPX

API testing relies on the high-performance \`httpx\` library. The driver fixture will yield an \`HttpxClient\` when the test is marked with \`@pytest.mark.api\`.

## Usage

\`\`\`python
import pytest

@pytest.mark.api
def test_get_users(driver):
    response = driver.get("/users/1")
    assert response.status_code == 200
    assert "name" in response.json()
\`\`\`

## Running Tests
Run all API tests:
\`\`\`bash
pytest -m api
\`\`\`
EOF
        echo "* [API Testing Guide](api-testing.md)" >> "$project_path/docs/README.md"
    elif [ "$mod" == "mobile" ]; then
cat <<EOF > "$project_path/docs/mobile-testing.md"
# Mobile Testing with Appium

Mobile testing connects to an Appium Server. Make sure your \`.env\` file has the correct \`APPIUM_SERVER_URL\` and \`PLATFORM_NAME\`.

## Usage

The \`AppiumDriver\` inherits from \`UiDriver\` and wraps the underlying WebDriver instance. You can access the raw Appium driver via \`driver.driver\` if you need native Appium commands.

## Running Tests
Run all Mobile tests:
\`\`\`bash
pytest -m mobile
\`\`\`
EOF
        echo "* [Mobile Testing Guide](mobile-testing.md)" >> "$project_path/docs/README.md"
    elif [ "$mod" == "contract" ]; then
cat <<EOF > "$project_path/docs/contract-testing.md"
# Contract Testing with Pact

Contract testing prevents breaking changes between microservices. The \`pact\` fixture provides a \`PactManager\` instance initialized with your consumer/provider names from \`.env\`.

## Usage

\`\`\`python
def test_contract(pact):
    expected_body = {"status": "up"}
    
    (pact
     .given("Service is up")
     .upon_receiving("a health check")
     .with_request("GET", "/health")
     .will_respond_with(200, body=expected_body))
     
    # Make request to pact.uri...
\`\`\`
EOF
        echo "* [Contract Testing Guide](contract-testing.md)" >> "$project_path/docs/README.md"
    elif [ "$mod" == "bdd" ]; then
cat <<EOF > "$project_path/docs/bdd-testing.md"
# BDD Testing with pytest-bdd

Behavior-Driven Development (BDD) testing uses \`pytest-bdd\` to write tests in natural language.

## Usage

Write features in \`tests/features/\` and implement step definitions in your test files. The framework automatically injects fixtures like \`driver\` into your step definitions.

\`\`\`python
from pytest_bdd import scenario, given, when, then

@scenario('features/sample.feature', 'Sample Scenario')
def test_sample():
    pass

@given("I have a driver")
def have_driver(driver):
    pass
\`\`\`
EOF
        echo "* [BDD Testing Guide](bdd-testing.md)" >> "$project_path/docs/README.md"
    fi
done

# Generate mkdocs.yml
cat <<EOF > "$project_path/mkdocs.yml"
site_name: Taflex Py Test Automation
site_description: Scaffolded test automation project with TAFLEX PY

theme:
  name: material
  custom_dir: docs/overrides
  features:
    - navigation.top
    - navigation.footer
    - navigation.indexes
    - search.suggest
    - search.highlight
    - search.share
    - content.code.copy
    - content.action.edit
  palette:
    - scheme: slate
      primary: yellow
      accent: yellow
  font:
    text: Inter
    code: JetBrains Mono

extra_css:
  - stylesheets/extra.css

markdown_extensions:
  - admonition
  - tables
  - attr_list
  - md_in_html
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.details
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.blocks.html
  - pymdownx.magiclink

nav:
  - Introduction: README.md
  - Core Architecture: core-architecture.md
  - Testing Guides:
EOF

for mod in "${modules[@]}"; do
    if [ "$mod" == "web" ]; then echo "    - Web Testing: web-testing.md" >> "$project_path/mkdocs.yml"; fi
    if [ "$mod" == "api" ]; then echo "    - API Testing: api-testing.md" >> "$project_path/mkdocs.yml"; fi
    if [ "$mod" == "mobile" ]; then echo "    - Mobile Testing: mobile-testing.md" >> "$project_path/mkdocs.yml"; fi
    if [ "$mod" == "contract" ]; then echo "    - Contract Testing: contract-testing.md" >> "$project_path/mkdocs.yml"; fi
    if [ "$mod" == "bdd" ]; then echo "    - BDD Testing: bdd-testing.md" >> "$project_path/mkdocs.yml"; fi
done

if [[ " ${reports[*]} " =~ " allure " ]]; then
cat <<EOF >> "$project_path/mkdocs.yml"
  - Execution Reports: allure-report/
EOF
fi

# Generate docs.sh script
cat <<EOF > "$project_path/docs.sh"
#!/bin/bash
echo "============================================"
echo "  taflex-py - Documentation Server"
echo "============================================"

# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo "📦 Installing MkDocs and Material theme..."
    pip install mkdocs-material mkdocs-mermaid2-plugin
fi

echo "🌐 Starting local documentation server at http://localhost:8000"
echo "💡 Press Ctrl+C to stop the server."

mkdocs serve
EOF
chmod +x "$project_path/docs.sh"

fi # End if [ "$req_docs" == "y" ]


# Generate config.sh script
cat <<EOF > "$project_path/config.sh"
#!/bin/bash
echo "============================================"
echo "  taflex-py - Environment Configuration"
echo "============================================"
echo "Setting up virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing project and dependencies..."
pip install -e ".[all]"
EOF

if [[ " ${modules[*]} " =~ " web " ]]; then
cat <<EOF >> "$project_path/config.sh"

echo "Installing Playwright browsers..."
playwright install
EOF
fi

cat <<EOF >> "$project_path/config.sh"

echo "============================================"
echo "✅ Setup complete! You can now run your tests."
echo "   Command: pytest"
echo "============================================"
EOF

# Make config.sh executable
chmod +x "$project_path/config.sh"

# Generate allure.sh if allure is selected
if [[ " ${reports[*]} " =~ " allure " ]]; then
cat <<EOF > "$project_path/allure.sh"
#!/bin/bash
echo "============================================"
echo "  taflex-py - Allure Report Generator"
echo "============================================"

# Check if allure command exists
if ! command -v allure &> /dev/null
then
    echo "❌ Error: 'allure' command not found."
    echo "   Please install Allure Commandline to view reports."
    echo "   Installation guide: https://allurereport.org/docs/install/"
    echo "   Example (macOS): brew install allure"
    exit 1
fi

echo "Generating and opening Allure report..."
allure serve reports/allure-results
EOF
chmod +x "$project_path/allure.sh"
fi

echo ""
echo "✅ Project scaffolded successfully at '$project_path'!"
echo ""
echo "Next steps for the team:"
echo "  1. cd $project_path"
echo "  2. source ./config.sh"
echo "  3. pytest"
echo "============================================"
