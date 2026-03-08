---
title: Scaffolding Wizard
---

# Scaffolding Wizard

The **TAFLEX PY Modular** framework includes an interactive, CLI-based Scaffolding Wizard (`scaffold.sh`) that dynamically generates a bespoke test automation project based on your specific requirements.

Instead of cloning a monolithic repository full of tools you don't need, the wizard asks you a series of questions and builds a lightweight, clean project tailored to your team's stack.

!!! tip "Fast Track"
    To generate a new project instantly, run the script from the root of the repository:
    ```bash
    ./scaffold.sh
    ```

<hr style="border-color: #2a2a2a; margin: 3rem 0;">

## Configuration Modules

The wizard allows you to build a custom tech stack. By selecting only what you need, you reduce dependency bloat.

### 1. Testing Domains

<div class="tx-grid">
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #ca8a04;">WEB</span>
    <h3>Playwright</h3>
    <p>Includes <code>taflex.web</code> and installs <code>playwright</code> dependencies. Select this for robust browser automation.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #22c55e;">API</span>
    <h3>HTTPX</h3>
    <p>Includes <code>taflex.api</code> and installs <code>httpx</code>. Select this for high-speed, direct backend API tests.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #8b5cf6;">MOBILE</span>
    <h3>Appium</h3>
    <p>Includes <code>taflex.mobile</code> and installs <code>Appium-Python-Client</code>. Select this for iOS/Android native app automation.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #f59e0b;">CONTRACT</span>
    <h3>Pact</h3>
    <p>Includes <code>taflex.contract</code> and installs <code>pact-python</code>. Select this for consumer-driven contract testing.</p>
  </div>
</div>

!!! info "Default Fallback"
    If no specific testing modules are selected, the wizard defaults to setting up the **Web Testing** domain.

### 2. Reporting Stack

Next, the wizard configures your enterprise reporting stack:

<div class="tx-grid">
  <div class="tx-card">
    <h3>📄 HTML Report</h3>
    <p>Generates a lightweight, single-file HTML report directly from <code>pytest-html</code>. Perfect for fast local debugging.</p>
  </div>
  <div class="tx-card">
    <h3>📊 Allure Report</h3>
    <p>Sets up <code>allure-pytest</code> integration for rich, interactive reporting. Includes a helper script to serve results locally.</p>
  </div>
  <div class="tx-card">
    <h3>🚀 ReportPortal</h3>
    <p>Sets up <code>pytest-reportportal</code> and populates the <code>.env</code> file with EPAM ReportPortal configurations.</p>
  </div>
  <div class="tx-card">
    <h3>🎯 Jira Xray</h3>
    <p>Sets up <code>pytest-jira-xray</code> to sync automated test results directly back to Jira Test Executions for full traceability.</p>
  </div>
</div>

### 3. CI/CD & Target Directory

- **CI/CD Pipelines:** Automatically generates CI/CD configuration files (e.g., GitHub Actions `ci.yml` or GitLab CI `.gitlab-ci.yml`) optimized with caching and linting.
- **Target Directory:** Define exactly where the new project should be generated (e.g., `./my-test-project`).

<hr style="border-color: #2a2a2a; margin: 3rem 0;">

## What Gets Generated?

The wizard seamlessly creates a ready-to-run environment containing:

1. **Source Code (`src/taflex/`)**: Copies the `core` module and your selected domain modules.
2. **Build System (`pyproject.toml`)**: Dynamically populates dependencies and Pytest markers based on your selections.
3. **Environment (`.env`)**: Sets the primary `EXECUTION_MODE` and prepares relevant sections (e.g., `APPIUM_SERVER_URL`).
4. **Scaffolding (`tests/` & `docs/`)**: Generates sample Page Objects, tests, local `conftest.py`, and custom documentation for your team.
5. **Quickstart Script (`config.sh`)**: A helper to instantly initialize the virtual environment, install dependencies, and download required binaries (like Playwright browsers).

## Next Steps

Once the wizard completes, your new project is ready to execute:

```bash
cd my-test-project
source ./config.sh
pytest
```