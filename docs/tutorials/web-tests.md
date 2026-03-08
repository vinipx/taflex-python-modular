# Web Testing Tutorial

Learn how to write robust and maintainable Web tests using TAFLEX PY.

## 1. Page Object Model (POM)

We recommend using the Page Object Model to encapsulate page-specific logic and locators. This makes tests readable and easy to maintain.

### Step 1: Create Locators
Create a JSON file for your page in `src/resources/locators/web/search.json`:

```json
{
  "search_input": "input[name='q']",
  "search_button": "input[type='submit'] >> n=1"
}
```

### Step 2: Create Page Object
Create a class to handle interactions in `tests/web/pages/search_page.py`:

```python
class SearchPage:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator('input[name="q"]')

    def open(self):
        self.page.goto('https://www.google.com')

    def search_for(self, term):
        self.search_input.fill(term)
        self.page.keyboard.press('Enter')
```

## 2. Writing the Test Spec

Use the `driver` fixture to inject the initialized strategy into your test.

```python
import re
from playwright.sync_api import expect
from .pages.search_page import SearchPage

def test_should_find_relevant_results(web_driver):
    search_page = SearchPage(web_driver.page)
    
    search_page.open()
    search_page.search_for('TAFLEX PY')
    
    # Assertions using Playwright's expect
    expect(web_driver.page).to_have_title(re.compile("TAFLEX PY"))
```

## 3. Best Practices

- **Load Locators Early**: Always call `driver.loadLocators('page_name')` before interacting with elements.
- **Use Logical Names**: Refer to elements by their logical names (e.g., `login_button`) instead of hardcoded CSS/XPath.
- **Leverage Fixtures**: Use the `driver` fixture to handle automatic browser lifecycle (startup/teardown).

## Running on Cloud Grids

You can run these same tests on **BrowserStack** or **SauceLabs** by simply updating your `.env` file. No code changes are required.

Refer to the [Cloud Execution Tutorial](./cloud-execution.md) for detailed configuration steps.
