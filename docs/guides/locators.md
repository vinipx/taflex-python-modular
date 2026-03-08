# Locators Management

TAFLEX PY uses a hierarchical JSON-based system for managing locators, allowing for clean separation and easy overrides.

## Directory Structure

```text
src/resources/locators/
├── global.json            # Application-wide locators
├── web/
│   ├── common.json        # Shared web locators
│   └── login.json         # Page-specific locators (Login)
├── api/
│   └── common.json
└── mobile/
    └── common.json
```

## Example: login.json

```json
{
    "username_field": "#username",
    "password_field": "#password",
    "login_button": "button[type='submit']"
}
```

## Usage in Tests

```python
def test_login(web_driver):
    web_driver.navigate_to('https://example.com/login')
    
    # Deprecated: The framework now favors POM over dynamic JSON locators for Web
    web_driver.load_locators('login')
    username = web_driver.find_element('username_field')
    username.fill('myuser')
```

The `findElement` method will resolve the logical name `username_field` to the CSS selector `#username`.
