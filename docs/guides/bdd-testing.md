# BDD Testing

TAFLEX PY supports Behavior-Driven Development (BDD) using Gherkin syntax through the `pytest-bdd` integration.

## Project Structure

BDD tests are located in the `tests/bdd/` directory:
- `features/`: Contains your `.feature` files (Gherkin).
- `test_*.py`: Contains your Python step definitions and scenario bindings.

## Writing a Feature File

Create a file `tests/bdd/features/login.feature`:

```gherkin
Feature: User Login

  Scenario: Successful login
    Given I navigate to "https://example.com/login"
    When I enter "myuser" as username and "mypass" as password
    And I click on the login button
    Then I should see "Welcome" in the header
```

## Writing Step Definitions

Create a Python file `tests/bdd/test_login_bdd.py`. Use the decorators from `pytest-bdd` and the TAFLEX PY `web_driver` fixture:

```python
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios from feature file
scenarios('features/login.feature')

@given(parsers.parse('I navigate to "{url}"'))
def navigate_to(web_driver, url):
    web_driver.navigate_to(url)

@when(parsers.parse('I enter "{username}" as username and "{password}" as password'))
def enter_credentials(web_driver, username, password):
    page = web_driver.page
    page.locator('#username').fill(username)
    page.locator('#password').fill(password)

@when('I click on the login button')
def click_login(web_driver):
    web_driver.page.locator('button[type="submit"]').click()

@then(parsers.parse('I should see "{expected}" in the header'))
def verify_header(web_driver, expected):
    from playwright.sync_api import expect
    expect(web_driver.page.locator('#flash')).to_contain_text(expected)
```

## Running BDD Tests

You can run BDD tests specifically using:

```bash
pytest tests/bdd/
```
