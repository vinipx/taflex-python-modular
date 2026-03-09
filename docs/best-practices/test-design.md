# Test Design Best Practices

## Page Object Model (POM)

We recommend using the Page Object Model (POM) to encapsulate page actions and logic. This maintains clean, readable tests and simplifies maintenance.

```python
from taflex.core.drivers.ui_driver import UiDriver

class LoginPage:
    def __init__(self, driver: UiDriver):
        self.driver = driver
        self.username_field = "#username"
        self.password_field = "#password"
        self.login_button = "button[type='submit']"

    def login(self, username, password):
        self.driver.type(self.username_field, username)
        self.driver.type(self.password_field, password)
        self.driver.click(self.login_button)
```

**Key Benefits:**
- **Encapsulation:** Locators and interaction logic are kept in one place.
- **Readability:** Tests describe "what" is happening (`login(user, pass)`), not "how" (selectors and clicks).
- **Maintainability:** Changes to selectors only require updating one file.

## Atomic Tests

Keep tests small and focused on a single capability. Each test should verify a specific business rule or interaction.

## Clean Data Strategy

For tests that require specific data states, use the `api_driver` fixture to set up test data via REST APIs before running UI-based scenarios. This is significantly faster and more reliable than setting up data via the UI.
