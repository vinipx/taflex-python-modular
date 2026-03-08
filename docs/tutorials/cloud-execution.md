# Testing in the Cloud

This tutorial will guide you through the process of executing your existing TAFLEX PY tests on **BrowserStack** or **SauceLabs**.

## Prerequisites

1.  A BrowserStack or SauceLabs account.
2.  Your **Username** and **Access Key** from the provider's dashboard.
3.  An existing TAFLEX PY project (follow the [Quick Start](../getting-started/quickstart.md) if you haven't yet).

---

## Step 1: Configure Environment Variables

The framework is designed to switch to cloud execution purely through configuration. Open your `.env` file and set the following:

### For BrowserStack
```env
CLOUD_PLATFORM=browserstack
CLOUD_USER=your_browserstack_username
CLOUD_KEY=your_browserstack_access_key

# Target Environment
OS=Windows
OS_VERSION=11
BROWSER=chromium
BROWSER_VERSION=latest
```

### For SauceLabs
```env
CLOUD_PLATFORM=saucelabs
CLOUD_USER=your_sauce_username
CLOUD_KEY=your_sauce_access_key

# Target Environment
OS=Windows 10
BROWSER=firefox
BROWSER_VERSION=latest
```

---

## Step 2: Execute Web Tests

Once the `.env` is configured, you don't need to change any code. Simply run your standard test command:

```bash
pytest tests/web
```

The framework will:
1.  Detect `CLOUD_PLATFORM` is not `local`.
2.  Build the required capabilities for the selected provider.
3.  Establish a remote WebSocket connection to the cloud grid.
4.  Execute the tests and stream results back to your terminal.

---

## Step 3: Execute Mobile Tests

To run mobile tests on real devices in the cloud:

1.  Update your `.env`:
    ```env
    EXECUTION_MODE=mobile
    CLOUD_PLATFORM=browserstack
    OS=Android
    OS_VERSION=Google Pixel 7
    ```
2.  Run the BDD or mobile specs:
    ```bash
    pytest tests/bdd
    ```

---

## Step 4: Verify in the Cloud Dashboard

After the execution starts, you can visit your provider's dashboard:

1.  **BrowserStack**: Go to the [Automate Dashboard](https://automate.browserstack.com).
2.  **SauceLabs**: Go to the [Automated Test Results](https://app.saucelabs.com/dashboard/tests).

You will see a new session named **"Playwright Web Test"** (for web) or **"WebdriverIO Mobile Test"** (for mobile) under the **"Taflex Framework"** project.

---

## 💡 Pro Tip: CLI Overrides

You can override your `.env` settings directly from the terminal to run a quick test on a different OS without changing files:

```bash
# Run on macOS Ventura using BrowserStack
OS="OS X" OS_VERSION="Ventura" CLOUD_PLATFORM="browserstack" pytest tests/web
```

## Troubleshooting

- **Invalid Credentials**: Ensure `CLOUD_USER` and `CLOUD_KEY` are correct. BrowserStack calls it an "Access Key," while SauceLabs calls it an "Access Key" as well.
- **Unsupported Platform**: Ensure the `OS` and `OS_VERSION` strings match what the provider expects (refer to their capability builders).
- **Network Issues**: Cloud execution requires a stable internet connection to stream browser commands.
