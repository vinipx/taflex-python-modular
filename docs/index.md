---
hide:
  - navigation
  - toc
---

<div class="tx-hero">
  <div class="tx-hero-badge">ENTERPRISE TEST AUTOMATION</div>
  <h1>TAFLEX PY</h1>
  <p class="tx-hero-subtitle">Unified Test Automation Framework for Web, API & Mobile</p>
  <p style="max-width: 800px; margin: 0 auto; color: #a1a1aa; line-height: 1.6;">
    A modern, enterprise-grade framework powered by Python, the Strategy Pattern, and externalized configuration — delivering unified test orchestration across every platform with zero code changes.
  </p>
  <div class="tx-hero-buttons">
    <a href="getting-started/quickstart/" class="tx-btn tx-btn-primary">Get Started &rarr;</a>
    <a href="architecture/overview/" class="tx-btn tx-btn-secondary">View Architecture</a>
  </div>
</div>

<hr style="border-color: #2a2a2a; margin: 4rem 0;">

## Multi-Platform Coverage

<p style="color: #a1a1aa;">Test across every platform channel in a single unified framework</p>

<div class="tx-grid">
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #ca8a04;">WEB</span>
    <h3>Web Testing (Playwright)</h3>
    <p>Playwright-powered browser automation with externalized locators, auto-wait strategies, and cross-browser support out of the box.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #22c55e;">API</span>
    <h3>API Testing (Dual Strategy)</h3>
    <p>Powerful API support using Playwright (Hybrid) for E2E flows and HTTPX (Specialized) with Pytest for high-speed standalone contract testing.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #8b5cf6;">MOBILE</span>
    <h3>Mobile Testing (Appium)</h3>
    <p>Native and hybrid mobile testing via Appium with shared locator management, parallel execution, and unified driver interface.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #0ea5e9;">CLOUD</span>
    <h3>Cloud Grids Support</h3>
    <p>Native integration with BrowserStack and SauceLabs to execute tests across thousands of real devices and browser combinations.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #ef4444;">AI-AGENT</span>
    <h3>Autonomous AI Ready</h3>
    <p>Native MCP (Model Context Protocol) server allows AI agents to run tests, inspect locators, and debug failures autonomously.</p>
  </div>
  <div class="tx-card">
    <span class="tx-badge" style="background-color: #f59e0b;">DATA</span>
    <h3>Database Integration</h3>
    <p>Native Postgres and MySQL support for test data setup, validation, and teardown — fully integrated into the test lifecycle.</p>
  </div>
</div>

<hr style="border-color: #2a2a2a; margin: 4rem 0;">

## Built for Enterprise

<p style="color: #a1a1aa;">Production-grade capabilities for mission-critical test automation</p>

<div class="tx-grid">
  <div class="tx-card">
    <h3>🤖 AI-Agent Integration (MCP)</h3>
    <p>Expose your test suite as an MCP server. Connect to Claude Desktop or IDE agents to transform your tests into an active AI service.</p>
  </div>
  <div class="tx-card">
    <h3>🤝 Pact Contract Testing</h3>
    <p>First-class support for Consumer-Driven Contracts. Catch breaking API changes early and ensure microservices compatibility at scale.</p>
  </div>
  <div class="tx-card">
    <h3>🧩 Strategy Pattern Architecture</h3>
    <p>Runtime driver resolution lets you switch between Web, API, and Mobile contexts. Native BDD support via Gherkin for human-readable specifications.</p>
  </div>
  <div class="tx-card">
    <h3>📄 Externalized Locators</h3>
    <p>All selectors stored in JSON files with Global -> Mode -> Page inheritance. Change locators without touching a single test file.</p>
  </div>
  <div class="tx-card">
    <h3>⚡ Fast Execution</h3>
    <p>Built on top of Playwright and Python for maximum performance and reliability on CI/CD pipelines and local development.</p>
  </div>
  <div class="tx-card">
    <h3>📊 Reporting Governance</h3>
    <p>Native Allure, ReportPortal, and Xray integration with detailed traces and videos for enterprise-level visibility and Jira traceability.</p>
  </div>
</div>

<hr style="border-color: #2a2a2a; margin: 4rem 0;">

## Quick Start

```bash
# Clone the repository
git clone https://github.com/vinipx/taflex-python-modular.git
cd taflex-python-modular

# Run the automated setup script
./setup.sh
source .venv/bin/activate

# Run all tests
pytest tests/

# Run unit tests
pytest tests/unit/
```
