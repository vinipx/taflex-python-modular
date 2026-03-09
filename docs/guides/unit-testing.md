# Unit & Framework Testing

TAFLEX PY uses **Pytest** for testing its core framework components. This ensures that the framework's logic (configuration, factory, drivers) is reliable independent of the automation engines.

## Running Framework Tests

```bash
pytest tests/framework
```

## Test Structure

Framework tests are located in `tests/framework/` and follow the `test_*.py` naming convention.

### AppConfig Tests
Verifies that environment variables are correctly validated using Pydantic Settings and that default values are applied.

### DriverFactory Tests
Checks that the correct driver strategy (`PlaywrightDriver`, `HttpxClient`, or `AppiumDriver`) is instantiated based on the `execution_mode` in the `AppConfig`.

### Driver Implementation Tests
Verifies that individual strategies (Web, API, Mobile) correctly implement the `UiDriver` or `ApiClient` interfaces and handle lifecycle events (`start`/`stop`).

## Mocking in Tests

We use Pytest's `unittest.mock` to isolate components during testing. For example, when testing the `DriverFactory`, we mock the driver classes to verify they are instantiated with the correct configuration without actually launching a browser or client.
