# TAFLEX PY Modular

[![CI](https://github.com/vinipx/taflex-python-modular/actions/workflows/ci.yml/badge.svg)](https://github.com/vinipx/taflex-python-modular/actions/workflows/ci.yml)
[![Docs](https://github.com/vinipx/taflex-python-modular/actions/workflows/docs.yml/badge.svg)](https://vinipx.github.io/taflex-python-modular/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**TAFLEX PY** is a high-performance, enterprise-grade test automation framework built on Python, designed for unified orchestration across **Web, API, Mobile, and Contract** testing.

By leveraging the **Strategy Pattern** and a modular architecture, TAFLEX PY allows teams to write tests once and execute them across multiple platforms and environments with zero code changes.

---

## 🚀 Key Features

- **Unified Driver Interface**: Single `driver` fixture for Playwright (Web), HTTPX (API), and Appium (Mobile).
- **Behavior-Driven Development (BDD)**: Native Gherkin support via `pytest-bdd` integration.
- **Enterprise Documentation**: Interactive, built-in MkDocs (Material theme) with automated CI/CD deployment.
- **Smart Scaffolding**: Interactive CLI wizard to generate lightweight, bespoke projects tailored to your tech stack.
- **Pact Contract Testing**: Full support for Consumer-Driven Contracts (compatible with `pact-python` v2 and v3+).
- **Hierarchical Locators**: Externalized JSON-based locator management with Global -> Mode -> Page inheritance.
- **AI-Ready (MCP)**: Built-in Model Context Protocol server, enabling AI agents to debug and run tests autonomously.
- **Cloud Grid Integration**: Native support for BrowserStack and SauceLabs.

---

## 🛠️ Quick Start

### 1. Installation
TAFLEX PY requires **Python 3.10+**.

```bash
# Clone the repository
git clone https://github.com/vinipx/taflex-python-modular.git
cd taflex-python-modular

# Run the automated setup script
./init.sh
source .venv/bin/activate
```

### 2. Project Scaffolding
Create a new, clean automation project using the interactive wizard:

```bash
./scaffold.sh
```
The wizard will ask which modules (Web, API, Mobile, Contract, BDD) and reporters (Allure, ReportPortal, Xray) you need, then generate a ready-to-run project directory.

### 3. Running Tests
```bash
# Run all tests
pytest

# Run tests with a specific marker
pytest -m web
pytest -m bdd
```

---

## 📚 Documentation

TAFLEX PY comes with comprehensive documentation.

- **Local Preview**: Run `./docs.sh` to start the local MkDocs server at `http://localhost:8000`.
- **Online Version**: [View the latest documentation here](https://vinipx.github.io/taflex-python-modular/).

---

## 🧩 Architecture

The framework follows a modular strategy where the `DriverFactory` resolves the correct automation engine at runtime based on your `.env` configuration or Pytest markers.

```mermaid
flowchart LR
    A[Test Suite] --> B[conftest.py]
    B --> C{DriverFactory}
    C --> D[Playwright Strategy]
    C --> E[HTTPX Strategy]
    C --> F[Appium Strategy]
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/contributing/guidelines.md) for more details.

---

## 📄 License

This project is licensed under the MIT License.
