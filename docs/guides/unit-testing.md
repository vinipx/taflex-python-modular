# Unit Testing

TAFLEX PY uses **Pytest** for unit testing its core components. This ensures that the framework's logic (configuration, locators, factory) is reliable independent of the automation engines.

## Running Unit Tests

```bash
pytest tests/unit
```

## Test Structure

Unit tests are located in `tests/unit/` and follow the `test_*.py` naming convention.

### ConfigManager Tests
Verifies that environment variables are correctly validated using Pydantic and that default values are applied.

### LocatorManager Tests
Ensures that locators are correctly merged from Global, Mode, and Page-specific JSON files.

### DriverFactory Tests
Checks that the correct driver strategy (Web, API, or Mobile) is instantiated based on the execution mode.

### DatabaseManager Tests
Mocks database drivers to verify that queries are correctly routed to PostgreSQL or MySQL connections.

## Mocking in Tests

We use Pytest's `monkeypatch / unittest.mock` to isolate components during testing, especially for filesystem operations (`fs`) and database drivers.
