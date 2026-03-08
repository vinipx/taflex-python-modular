# Test Design Best Practices

## Page Object Model (POM)
Even with hierarchical locators, we recommend using the Page Object Model to encapsulate page actions.

```python
class LoginPage:
    def __init__(self, page):
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('button[type="submit"]')

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

## Atomic Tests
Keep tests small and focused on a single capability.

## Clean Data Setup
Use the `DatabaseManager` to set up and tear down test data before and after execution.
