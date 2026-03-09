# Core API Reference

This page documents the primary interfaces and classes provided by TAFLEX PY.

## UiDriver & ApiClient (Abstract Classes)

The base protocols for all automation strategies (UI and API).

### UiDriver Methods

| Method | Description |
|--------|-------------|
| `start()` | Initializes the driver session (e.g., launches browser or app). |
| `stop()` | Closes the driver session. |
| `navigate(url)` | Navigates to the specified URL. |
| `click(selector)` | Clicks an element by its selector. |
| `type(selector, text)` | Types text into an element. |
| `get_text(selector)` | Returns the inner text of an element. |
| `is_visible(selector)` | Returns `True` if the element is visible. |
| `wait_for_selector(selector)` | Waits for an element to appear in the DOM. |
| `screenshot(path)` | Takes a screenshot and saves it to the path. |

### ApiClient Methods

| Method | Description |
|--------|-------------|
| `start()` | Initializes the API client session. |
| `stop()` | Closes the client session. |
| `get(url, **kwargs)` | Performs an HTTP GET request. |
| `post(url, **kwargs)` | Performs an HTTP POST request. |
| `put(url, **kwargs)` | Performs an HTTP PUT request. |
| `patch(url, **kwargs)` | Performs an HTTP PATCH request. |
| `delete(url, **kwargs)` | Performs an HTTP DELETE request. |

## AppConfig

The configuration class powered by Pydantic Settings.

| Attribute | Default | Description |
|-----------|---------|-------------|
| `execution_mode` | `"web"` | Execution target: `web`, `api`, or `mobile`. |
| `environment` | `"qa"` | Target environment for `base_url` resolution. |
| `browser` | `"chromium"` | Playwright browser to use (`chromium`, `firefox`, `webkit`). |
| `timeout_ms` | `30000` | Global timeout for operations in milliseconds. |
