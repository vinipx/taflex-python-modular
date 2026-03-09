---
sidebar_position: 2
title: Framework Execution Flow
---

# Framework Execution Flow

A common question when setting up or extending TAFLEX PY is: **"If we have specific fixtures in `conftest.py` like `web_driver` or `api_driver`, why do we still need the `DriverFactory`, the `EXECUTION_MODE` environment variable, and unit tests for the factory?"**

This document explains the "Why" behind the framework's execution flow and the Strategy Pattern architecture.

## 1. Why do we need `EXECUTION_MODE` in `.env`?

While you might have specific tests that explicitly request a `web_driver` or `api_driver`, the framework also provides a generic `driver` fixture in `conftest.py`. The behavior of this generic fixture is controlled by the `EXECUTION_MODE` variable.

### Use Cases:
* **Global Test Runs (BDD):** In Behavior-Driven Development (Cucumber/Gherkin), step definitions usually rely on a single, global `driver` fixture. By changing `EXECUTION_MODE=web` or `EXECUTION_MODE=mobile` in your `.env` (or CI/CD matrix), you can run the exact same scenarios against a web browser or a mobile device without altering a single line of test code.
* **Hybrid Frameworks:** It sets the "default" behavior of the framework. If a standard test doesn't explicitly request a specific driver type, it inherits the global environment setting.

## 2. Why do we need the Strategy Pattern (`DriverFactory` & Strategies)?

The Pytest fixtures in `conftest.py` determine *when* a driver is created (e.g., function scope, session scope). The Strategy pattern determines *how* it is created.

* **Separation of Concerns:** `conftest.py` should act as a lightweight routing layer. It should not contain hundreds of lines of code detailing how to configure Playwright context options, parse BrowserStack capabilities for Appium, or set up HTTPX headers. The `DriverFactory` handles the complexity of instantiating the correct engine.
* **Uniform Interface:** Because of the Strategy pattern, `conftest.py` can blindly call `driver.start()` and `driver.stop()` on **any** type of driver. The test runner doesn't care if it's shutting down an API session or closing a mobile emulator.
* **Extensibility:** If your team decides to switch from `httpx` to `requests` for APIs, or add a `mac_desktop` execution mode, you simply create a new Strategy class and register it in the `DriverFactory`. Your `conftest.py` and your test specs remain completely untouched.

## 3. Why test the Factory? (`test_factory.py`)

You will notice unit tests like `test_driver_factory_creates_web_driver` in the `tests/framework/` directory.

While `conftest.py` is integration-level code that actually spins up real browsers or APIs (which is slow and requires external dependencies), the unit test exists to verify the **routing logic** of the Factory in complete isolation. 

It ensures that if someone passes `EXECUTION_MODE="api"`, the framework accurately routes that configuration to the `HttpxClient` class. This protects the core architectural routing from regressions without the overhead of launching an actual browser session.

## Summary

* **Specific Fixtures (`web_driver`, `api_driver`)**: Used for tests that explicitly require a specific interface regardless of the global run (e.g., an API test creating test data immediately before a Web UI test runs).
* **`.env` / `EXECUTION_MODE`**: Drives the global default environment, crucial for CI/CD matrices and BDD step definitions.
* **Strategy Pattern (`DriverFactory`)**: Hides the complex configuration details of third-party libraries (Playwright/Appium/HTTPX) away from your Pytest layer, ensuring a unified and extensible API.
