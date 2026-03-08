# Reporting Governance

TAFLEX PY provides a robust reporting ecosystem designed to satisfy different stakeholders, from Developers needing quick feedback to Managers requiring high-level quality governance.

## Strategy: Choosing the Right Tool

Depending on your project's maturity and requirements, you might want to use one or a combination of these tools:

| Tool | Primary Audience | Best For... | Why use it? |
| :--- | :--- | :--- | :--- |
| **HTML Report** | Developers / QAs | Local debugging | Fast, zero-config, includes traces and videos. |
| **Allure** | QA / Dev Teams | Sprint-level results | Beautiful interactive charts, history, and categories. |
| **ReportPortal** | Managers / DevOps | Multi-project visibility | AI-powered failure analysis and cross-build trends. |
| **Xray (Jira)** | Managers / POs | Requirements Traceability | Links automated results directly to Jira User Stories. |

### Combining Tools
It is common and recommended to combine these tools. For example:
- **HTML + Xray**: Use HTML reports in CI for technical debugging and Xray to keep the business updated on Jira.
- **Allure + ReportPortal**: Use Allure for detailed team-level analysis and ReportPortal for long-term executive dashboards.

---

## 🛠 Xray Integration (Jira)

Xray is the preferred choice for teams requiring strict **Governance** and **Traceability**.

### Configuration
Enable it in your `.env`:
```bash
REPORTERS=html,xray
XRAY_ENABLED=true
XRAY_CLIENT_ID=your_id
XRAY_CLIENT_SECRET=your_secret
XRAY_PROJECT_KEY=PROJ
```

### Traceability Mapping
Tag your tests with Jira Issue Keys:
- **BDD**: `@PROJ-123 Scenario: ...`
- **Scripted**: `@pytest.mark.PROJ_123` or naming `test_PROJ_123_login`

---

## 📊 Allure Report

Allure is an open-source framework designed to create interactive and easy-to-read reports.

### Setup
1. Add `allure` to your `REPORTERS` in `.env`.
2. Results will be generated in `allure-results/`.

### Viewing Reports
```bash
# Install allure command line
npm install -g allure-commandline

# Generate and open report
allure serve allure-results
```

---

## 🚀 EPAM ReportPortal

ReportPortal is an AI-powered dashboard used for enterprise-scale test management.

### Configuration
Add `reportportal` to your `REPORTERS` and configure the connection:
```bash
RP_ENDPOINT=https://rp.yourcompany.com/api/v1
RP_API_KEY=your_key
RP_PROJECT=my_project
RP_LAUNCH=daily_smoke_tests
```

### Why use it?
- **AI Analysis**: Automatically categorizes failures (Product Bug, Automation Bug, System Issue).
- **Consolidated View**: See results from different pipelines and languages in a single place.

---

## 📝 Built-in HTML Report

The standard Playwright HTML report is always available for deep technical inspection.

- **Traces**: View step-by-step execution with DOM snapshots.
- **Videos/Screenshots**: Attached automatically on failure.
- **Usage**: Typically used during local development or as a CI artifact.
