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
deps=("pytest" "pydantic" "pydantic-settings" "SQLAlchemy" "ruff" "mypy" "pytest-xdist")

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

# Copy selected modules
for mod in "${modules[@]}"; do
    if [ -d "$TEMPLATE_DIR/src/taflex/$mod" ]; then
        cp -R "$TEMPLATE_DIR/src/taflex/$mod" "$project_path/src/taflex/"
    fi
done

# Handle CI/CD configuration
if [ "$ci_type" == "github" ]; then
    echo "Configuring GitHub Actions..."
    if [ -d "$TEMPLATE_DIR/.github" ]; then
        cp -R "$TEMPLATE_DIR/.github" "$project_path/"
        # Update GitHub CI to use pip install -e .
        sed -i '' 's/pip install -r requirements.txt/pip install -e ./' "$project_path/.github/workflows/ci.yml" 2>/dev/null || \
        sed -i 's/pip install -r requirements.txt/pip install -e ./' "$project_path/.github/workflows/ci.yml"
    else
        echo "⚠️  Template .github directory not found!"
    fi
elif [ "$ci_type" == "gitlab" ]; then
    echo "Configuring GitLab CI..."
cat <<EOF > "$project_path/.gitlab-ci.yml"
image: python:3.10

stages:
  - build
  - lint

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
EOF
fi

# Generate pyproject.toml (Modern standard)
echo "Generating pyproject.toml..."

# Prepare dependencies strings for TOML
base_deps="\"pytest\", \"pydantic\", \"pydantic-settings\", \"SQLAlchemy\", \"ruff\", \"mypy\", \"pytest-xdist\""
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
done
echo "all = [\"taflex-py-project[$(IFS=,; echo "${modules[*]}")]\"]" >> "$project_path/pyproject.toml"

cat <<EOF >> "$project_path/pyproject.toml"

[tool.pytest.ini_options]
addopts = "$pytest_addopts"
testpaths = ["tests"]
pythonpath = ["src"]
filterwarnings = [
    "ignore::DeprecationWarning:pytest_reportportal.plugin",
]
markers = [
    "api: mark test as api test",
    "web: mark test as web test",
    "mobile: mark test as mobile test",
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
from tests.pages.app_page import AppPage

@pytest.mark.mobile
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
    fi
done

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
