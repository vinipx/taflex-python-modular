# Developers Guide

This guide is for developers who want to extend TAFLEX PY or integrate it into their CI/CD pipelines.

## Extending the Framework

### Adding a New Strategy
To add support for a new platform, create a new class extending `UiDriver` or `ApiClient` in `src/core/drivers/strategies/`.

```python
from src.core.drivers.ui_driver import UiDriver

class MyNewStrategy(UiDriver):
    # Implement abstract methods
    pass
```

Then, register it in `src/core/drivers/driver_factory.py`.

## BDD Integration (Gherkin)

TAFLEX PY uses `pytest-bdd` to bridge Gherkin and Playwright.

### Generation Process
When running BDD tests, the framework executes `pytest-bdd`. This command:
1. Scans `tests/bdd/features/*.feature`.
2. Scans `tests/bdd/test_*.py` for step definitions.
3. Automatically binds Gherkin steps to Python functions during the Pytest run.

## Unit Testing

Always add unit tests for core framework logic. We use **Pytest** for its speed and modern API.

```bash
pytest tests/unit
```

## CI/CD Integration

TAFLEX PY is designed to run in headless environments. Ensure you pass the required environment variables.

### GitHub Actions Example
```yaml
- name: Run tests
  run: pytest tests/
  env:
    BASE_URL: ${{ secrets.BASE_URL }}
    API_BASE_URL: ${{ secrets.API_BASE_URL }}
```

## Type Safety with Pydantic

If you add new configuration parameters, update the `ConfigSchema` in `src/config/config_manager.py`. This ensures that any missing or invalid configuration is caught immediately at runtime.

## Code Hygiene & Formatting

To maintain high code quality and consistency across the project, we use **Ruff** and **Mypy**.

### Linting
Checks for potential errors and adherence to coding standards:
```bash
ruff check . && mypy src/
```

### Automatic Formatting
Fixes formatting and simple linting issues automatically:
```bash
ruff check --fix .
```

All contributions must pass the linter before being merged into the main branch.
