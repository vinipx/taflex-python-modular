# Mobile Testing Tutorial

Learn how to automate native and hybrid mobile applications using TAFLEX PY and **Appium**.

## 1. Environment Setup

Mobile testing requires the `mobile` strategy. Ensure you have Appium and the necessary drivers (like `uiautomator2`) installed.

### Installing Appium (Local)
If you are running tests against a physical device or local emulator:

```bash
# Install Appium Server
npm install -g appium

# Install Android Driver
appium driver install uiautomator2
```

### Starting the Server
```bash
appium --log-level info
```

## 2. Writing a Mobile Test

Set the `EXECUTION_MODE=mobile` in your `.env` or use the `mobile_driver` fixture. TAFLEX PY provides a unified element wrapper (`MobileElement`) that works identically to the web elements.

### Step 1: Create Locators
Create a JSON file in `src/resources/locators/mobile/settings.json`:

```json
{
  "system_settings_title": "//*[@text='Settings' or @text='Config' or @text='Configurações']",
  "search_box": "//*[contains(@resource-id, 'search') or contains(@content-desc, 'Search')]",
  "search_input": "//*[contains(@class, 'EditText')]"
}
```

### Step 2: Create the Test Spec
Create a file `tests/mobile/test_android_settings.py`:

```python
import pytest
import allure
from src.core.utils.logger import logger

@allure.feature('Mobile App')
@allure.story('Android System Settings')
@pytest.mark.mobile
def test_android_settings_interaction(mobile_driver):
    driver = mobile_driver
    
    # 1. Load the mobile locators
    driver.load_locators('settings')
    
    # 2. Interact with the UI using the unified API
    title_element = driver.find_element('system_settings_title')
    title_element.wait_for(timeout=10)
    assert title_element.is_visible() is True

    # 3. Take a screenshot
    driver.capture_screenshot('settings_home_page')
    
    # 4. Perform complex interactions
    search_box = driver.find_element('search_box')
    search_box.wait_for()
    search_box.click()
    
    search_input = driver.find_element('search_input')
    search_input.wait_for()
    search_input.fill('Battery')
    
    driver.capture_screenshot('settings_search_page')
```

## 3. Best Practices

- **Lazy Elements**: Elements in TAFLEX PY are **Lazy**. They aren't searched for until you perform an action (click, fill, etc.), which makes them much more resilient to slow mobile transitions.
- **Wait Strategies**: Always use `element.wait_for()` before critical actions on mobile devices.
- **Locator Fallbacks**: Use broad XPaths in your locator files to ensure compatibility across different Android device manufacturers (Samsung, Pixel, etc.).

## 4. Execution on Real Devices (Cloud)

While local execution is great for development, TAFLEX PY allows you to run these tests on **real devices** via BrowserStack and SauceLabs.

Configure your `.env` with your cloud credentials:

```env
EXECUTION_MODE=mobile
CLOUD_PLATFORM=browserstack
CLOUD_USER=your_user
CLOUD_KEY=your_key
OS=Android
OS_VERSION=13.0
```

Refer to the [Cloud Execution Tutorial](./cloud-execution.md) for more details.
