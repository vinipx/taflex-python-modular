---
sidebar_position: 1
title: Quick Start
---

# Quick Start Guide

Get up and running with TAFLEX PY in under 5 minutes.

## 1. Installation

TAFLEX PY requires **Python 3.10** or higher. We provide a setup script to automatically configure your virtual environment, install dependencies, and download Playwright browsers.

```bash
# Clone the repository
git clone https://github.com/vinipx/taflex-python-modular.git
cd taflex-python-modular

# Run the setup script
./setup.sh

# Activate the virtual environment
source .venv/bin/activate
```

## 2. Configuration

The `setup.sh` script automatically creates a `.env` file from the `.env.example` template if one doesn't exist. Open the `.env` file to customize your execution environment:

```env
EXECUTION_MODE=web
BROWSER=chromium
HEADLESS=true
BASE_URL=https://www.google.com
API_BASE_URL=https://jsonplaceholder.typicode.com

# Reporting configuration
REPORTERS=html,allure
```

## 3. Running Your First Test

### Integration Tests (Web/API)
Execute the Pytest test suite:

```bash
# Run all tests
pytest tests/

# Run a specific spec
pytest tests/web/test_login.py
```

### Unit Tests
Verify the framework core components:

```bash
pytest tests/unit/
```

## 4. Visualizing Results

For enterprise reporting, generate the Allure report:

```bash
allure serve allure-results
```

---

## 🏗️ What's Next?

- [Scaffolding Wizard](scaffolding-wizard.md)
- [Architecture Overview](../architecture/overview.md)
- [How to manage Locators](../guides/locators.md)
