# Cloud Testing Guide

TAFLEX PY provides native integration with industry-leading cloud testing platforms like **BrowserStack** and **SauceLabs**. This allows you to scale your test execution across a vast array of browser/OS combinations and real mobile devices without managing your own infrastructure.

## 🚀 Why Use Cloud Testing?

- **Zero Infrastructure**: No need to maintain local browser versions or mobile emulators.
- **Parallel Execution**: Run tests simultaneously across multiple configurations.
- **Real Devices**: Test your mobile applications on actual physical hardware.
- **Debugging Tools**: Access video recordings, network logs, and screenshots of every test session.

## 🛠️ Configuration

To enable cloud execution, update your `.env` file with the following parameters:

### Common Settings

```env
# Set the platform (local, browserstack, saucelabs)
CLOUD_PLATFORM=browserstack

# Your cloud credentials
CLOUD_USER=your_username
CLOUD_KEY=your_access_key
```

### Web Execution

For web automation, you can specify the target environment:

```env
EXECUTION_MODE=web
BROWSER=chromium
BROWSER_VERSION=latest
OS=Windows
OS_VERSION=11
```

### Mobile Execution

For mobile automation, the framework automatically maps these settings to Appium capabilities:

```env
EXECUTION_MODE=mobile
OS=Android
OS_VERSION=Google Pixel 7
```

---

## 🌩️ Supported Providers

### BrowserStack

When `CLOUD_PLATFORM=browserstack` is set, the framework uses the Playwright CDP (Chrome DevTools Protocol) endpoint for web tests and the BrowserStack Appium hub for mobile tests.

**Specific capabilities included:**
- `bstack:options` are automatically generated.
- Project and Build names are automatically tagged with "Taflex Framework" and the current date.

### SauceLabs

When `CLOUD_PLATFORM=saucelabs` is set, the framework connects to the SauceLabs US-West-1 data center.

**Specific capabilities included:**
- `sauce:options` are automatically generated.
- Standard W3C capabilities are enforced for maximum compatibility.

---

## 💻 CLI Usage

You can easily switch between local and cloud execution using environment variables in your command line:

```bash
# Run web tests locally
pytest tests/web

# Run web tests on BrowserStack
CLOUD_PLATFORM=browserstack pytest tests/web

# Run mobile tests on SauceLabs
CLOUD_PLATFORM=saucelabs EXECUTION_MODE=mobile pytest tests/mobile
```

## 🔍 Debugging in the Cloud

Once a test finishes, you can log in to your provider's dashboard to see:
1. **Video Recording**: A full video of the test execution.
2. **Metadata**: Detailed information about the browser, OS, and environment.
3. **Logs**: Console logs and network traffic (HAR files).
