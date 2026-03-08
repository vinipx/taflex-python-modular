# API Testing

TAFLEX PY employs a **Dual API Strategy** that allows you to choose the best tool for your specific testing needs.

| Strategy | Engine | Best For... |
|----------|--------|-------------|
| **Hybrid (E2E)** | Playwright | API calls within UI flows (setup/teardown), shared authentication with browser context. |
| **Specialized (Logic)** | HTTPX + Pytest | High-volume contract testing, complex business logic validation, and standalone API suites requiring maximum execution speed. |

---

## 1. Hybrid API Testing (Playwright)

This strategy uses Playwright's `APIRequestContext`.

## Configuration

Ensure `API_BASE_URL` is set in your `.env` file.

## Writing an API Test

Use the `api_driver` fixture (or a generic driver with `EXECUTION_MODE=api`).

```python
import pytest

@pytest.mark.api
def test_get_user_details(api_driver):
    response = api_driver.get('/users/1')
    assert response.status == 200
    
    user = response.json()
    assert user['username'] == 'Bret'
```

## Available Methods

The API driver supports standard HTTP methods:
- `driver.get(url, **kwargs)`
- `driver.post(url, **kwargs)`
- `driver.put(url, **kwargs)`
- `driver.delete(url, **kwargs)`

## 2. Specialized API Testing (HTTPX + Pytest)

For high-performance, pure API tests (without UI dependencies), TAFLEX PY supports a specialized strategy using **HTTPX**.

### Configuration
Set the provider in your `.env`:
```env
API_PROVIDER=httpx
```

### Writing an HTTPX API Test
Create a file `test_users.py` in your `tests/api/` directory:

```python
import pytest

@pytest.mark.api
def test_fetch_data(api_driver):
    response = api_driver.get('/endpoint')
    assert response.status_code == 200
    
    data = response.json()
    assert 'id' in data
```

### Running Specialized Tests
```bash
pytest tests/api/
```
