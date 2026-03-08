# API Testing Tutorial

Learn how to master the **Dual API Strategy** in TAFLEX PY. Choose the right tool for the right job: Playwright for integrated flows or HTTPX for high-performance specialized tests.

---

## 1. Hybrid Approach (Playwright)

**Use case:** Integrated tests where you need to share authentication with a browser or see API calls in a Trace Viewer.

### Creating the Test
Create a standard Playwright spec in `tests/api/`:

```python
import pytest

@pytest.mark.api
def test_hybrid_api_strategy(api_driver):
    # Perform request
    response = api_driver.get('/users/1')
    
    # Assert
    assert response.status == 200
    user = response.json()
    assert user['username'] == 'Bret'
```

**How to run:**
```bash
pytest tests/api/
```

---

## 2. Specialized Approach (HTTPX + Pytest)

**Use case:** Standalone API testing, contract validation, and extreme execution speed.

### Creating the Test
Create a file ending in `test_*.py` in `tests/api/`. These tests use **Pytest** as the runner.

```python
import pytest
from src.core.drivers.driver_factory import DriverFactory

@pytest.fixture(scope="module")
def httpx_driver():
    # Ensure API_PROVIDER=httpx is set in .env
    driver = DriverFactory.create('api') 
    await driver.initialize({
        api_base_url: 'https://jsonplaceholder.typicode.com'
    })
    yield driver
    driver.terminate()

def test_specialized_api_strategy(httpx_driver):
    # 2. Perform request
    response = httpx_driver.get('/users/1')

    # 3. Standard Pytest assertions
    assert response.status_code == 200
    user = response.json()
    assert user['id'] == 1
```

**How to run:**
```bash
# Set provider if not default in .env
API_PROVIDER=httpx pytest tests/api/
```

---

## 3. Which one should I choose?

| Feature | Playwright Strategy | HTTPX Strategy |
|---------|---------------------|----------------|
| **Runner** | Playwright | Pytest |
| **Speed** | Moderate | Fast (Blazing) |
| **Trace Viewer** | Yes | No |
| **Authentication Sharing** | Native with Browser | Manual |
| **Watch Mode** | `pytest --headed` (Using pytest-playwright) | `pytest-watch` (Auto-watch) |

---

## 4. Best Practices

- **Shared Locators**: Use `src/resources/locators/api/common.json` to store endpoints for both strategies.
- **Environment URLs**: Always rely on `API_BASE_URL` in your `.env`.
- **Validation**: For both strategies, the `driver` wrapper provides consistent `status()`, .json()`, and `ok()` methods to keep your code portable.
