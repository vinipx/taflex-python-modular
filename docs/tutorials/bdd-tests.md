# BDD Testing Tutorial

In this tutorial, you will learn how to create and run a Behavior-Driven Development (BDD) test using Gherkin syntax.

## 1. Create a Feature File

Features are defined in `.feature` files using plain English. Create a file at `tests/bdd/features/google_search.feature`:

```gherkin
Feature: Google Search

  Scenario: Searching for TAFLEX PY
    Given I navigate to "https://www.google.com"
    When I search for "TAFLEX PY"
    Then I should see results related to "TAFLEX"
```

## 2. Implement Step Definitions

Step definitions bridge the Gherkin steps to actual code. Create `tests/bdd/test_google.py`:

```python
from pytest_bdd import scenarios, given, when, then, parsers

# Load scenarios from feature file
scenarios('features/google_search.feature')

@given(parsers.parse('I navigate to "{url}"'))
def navigate(web_driver, url):
    web_driver.navigate_to(url)

@when(parsers.parse('I search for "{term}"'))
def search(web_driver, term):
    web_driver.load_locators('global') # Using global locators
    search_input = web_driver.find_element('search_input')
    search_input.fill(term)
    search_input.press('Enter')

@then(parsers.parse('I should see results related to "{expected}"'))
def verify_results(web_driver, expected):
    # Assertions using TAFLEX PY unified element API
    body_text = web_driver.page.text_content('body')
    assert expected in body_text
```

## 3. Run the Test

Execute the BDD-specific test command:

```bash
pytest tests/bdd
```

## Key Benefits of this Approach

1. **Shared State**: The `driver` fixture is shared between all steps in a scenario.
2. **Locator Management**: You can use `driver.loadLocators()` within any step to fetch your JSON-based selectors.
3. **Enterprise Reporting**: BDD scenarios appear beautifully in Allure and ReportPortal, showing each Gherkin step as a test phase.
