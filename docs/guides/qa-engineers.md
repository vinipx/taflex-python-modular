# QA Engineers Guide

This guide is designed for QA Engineers who will be using TAFLEX PY to write and maintain automated tests.

## Locator Management

One of the most powerful features of TAFLEX PY is hierarchical locator management. You don't need to touch the code to update a selector.

### How to update a locator
1. Locate the corresponding JSON file in `src/resources/locators`.
2. Update the value for the logical name.
3. Save the file and rerun the test.

**Resolution Order:**
- **Page-specific**: Highest priority.
- **Mode-specific**: Shared across a platform (e.g., all Web tests).
- **Global**: Fallback for application-wide elements.

## Writing Readable Tests

Use the `driver` fixture to keep your tests clean and focused on business logic.

```python
def test_verify_account_balance(web_driver):
    web_driver.navigate_to('/accounts')
    page = web_driver.page
    expect(page.locator('.total-balance')).to_have_text('$1,000.00')
```

## Behavior-Driven Development (BDD)

TAFLEX PY natively supports Gherkin syntax, allowing you to write specifications that are both executable and readable by non-technical team members.

- **Human Readable**: Define features and scenarios in plain English.
- **Unified Engine**: Reuse the same locators and drivers as standard tests.
- **Collaborative**: Perfect for refinement sessions with POs and stakeholders.

For a deep dive into writing and running BDD tests, see the [BDD Testing Guide](./bdd-testing.md).

## Troubleshooting Failures

- **Screenshots**: Automatically captured on failure in `test-results/`.
- **Traces**: Playwright traces allow you to step through the execution. Run `playwright show-trace path/to/trace.zip`.

## Reporting & Integration

TAFLEX PY supports multiple reporting tools like **Allure**, **ReportPortal**, and **Xray (Jira)**. These can be configured via the `REPORTERS` environment variable.

For a comprehensive guide on how to configure and choose between these tools, see the [Reporting & Governance Guide](./reporting.md).

### Allure Report
Allure provides rich, interactive test reports.
1. **Configuration**: Set `ALLURE_RESULTS_DIR` in `.env` (defaults to `allure-results`).
2. **View Report**:
   ```bash
   npm install -g allure-commandline
   allure serve allure-results
   ```

### EPAM ReportPortal
For enterprise-level test management, TAFLEX PY integrates with ReportPortal.
1. **Enable**: Add `reportportal` to `REPORTERS`.
2. **Configure**: Provide your instance details in `.env`:
   ```env
   RP_ENDPOINT=https://rp.yourcompany.com/api/v1
   RP_API_KEY=your_secret_key
   RP_PROJECT=your_project_name
   RP_LAUNCH=taflex-python-modular-automation
   RP_DESCRIPTION=Smoke Tests Execution
   RP_ATTRIBUTES=env:dev;team:qa
   ```

### Xray (Jira Integration)
Xray allows you to sync automated test results directly with Jira for full traceability.

1. **Enable**: Add `xray` to `REPORTERS`.
2. **Tag your tests**: Ensure your scenarios or tests contain the Jira Issue Key (e.g., `@PROJ-123`).
3. **Configure**: Provide credentials in `.env`:
   ```env
   XRAY_ENABLED=true
   XRAY_CLIENT_ID=your_id
   XRAY_CLIENT_SECRET=your_secret
   XRAY_PROJECT_KEY=PROJ
   ```

For a comprehensive setup guide, see the [Reporting & Xray Guide](./reporting.md).
