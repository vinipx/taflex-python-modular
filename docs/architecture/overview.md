---
sidebar_position: 1
title: Architecture Overview
---

# Architecture Overview

TAFLEX PY is built on a robust, extensible architecture that follows enterprise-grade design patterns. This document explains the architectural decisions and how different components interact.

## Design Philosophy

TAFLEX PY follows these core principles:

| Principle | Description |
|-----------|-------------|
| **🧩 Strategy Pattern** | Runtime driver resolution allows the same test code to run on Web, API, or Mobile without modification. |
| **📄 Separation of Concerns** | Test logic is completely decoupled from driver implementation and locator definitions. |
| **⚙️ Configuration Over Code** | Behavior is controlled through external configuration, not hardcoded values. |
| **🧪 Fast Feedback Loop** | High-performance execution using Playwright and Pytest for rapid development. |

## High-Level Architecture

```mermaid
flowchart TB
    subgraph "Test Layer"
        TC[Test Specs]
        BDD[BDD Features]
        FIX[Fixtures]
    end

    subgraph "Framework Core"
        DF[DriverFactory]
        LM[LocatorManager]
        CM[ConfigManager]
        DB[DatabaseManager]
    end

    subgraph "Driver Strategies"
        direction TB
        ADS[UiDriver & ApiClient<br/>Protocols]
        PDS[PlaywrightStrategy]
        APIS[PlaywrightApiStrategy]
        HXP[HttpxApiStrategy]
        AMS[AppiumMobileStrategy]
    end

    subgraph "Element Wrappers"
        PE[PlaywrightElement]
        ME[MobileElement]
    end

    subgraph "External Resources"
        JSON[JSON Locators]
        DATA[Test Data]
        ALR[Allure Reports]
    end

    TC --> FIX
    BDD --> FIX
    FIX --> DF
    FIX --> CM

    DF --> ADS
    ADS --> PDS
    ADS --> APIS
    ADS --> HXP
    ADS --> AMS

    PDS --> PE
    AMS --> ME

    ADS --> LM
    LM --> JSON

    TC --> DB
    DB --> DATA
```

## Component Breakdown

### 1. Driver Layer

The Driver Layer implements the **Strategy Pattern**, allowing runtime selection of the appropriate driver implementation.

```mermaid
classDiagram
    class UiDriver {
        <<abstract>>
        +initialize()
        +terminate()
        +navigate_to(str)
    }
    class ApiClient {
        <<abstract>>
        +initialize()
        +terminate()
        +get(str)
    }

    class PlaywrightStrategy {
        -browser
        -context
        -page
        +initialize()
        +navigate_to(str)
    }

    class PlaywrightApiStrategy {
        -requestContext
        +get(str)
        +post(str, dict)
    }

    class AppiumMobileStrategy {
        -client
        +initialize()
        +navigate_to(str)
    }

    class HttpxApiStrategy {
        -client
        +get(str)
        +post(str, dict)
    }

    UiDriver <|-- PlaywrightStrategy
    ApiClient <|-- PlaywrightApiStrategy
    ApiClient <|-- HttpxApiStrategy
    UiDriver <|-- AppiumMobileStrategy
```

**Key Benefits:**
- ✅ Single test codebase for all platforms.
- ✅ Driver changes (e.g., swapping engines) don't affect test specs.
- ✅ Supports parallel execution with different strategies.

### 2. Locator System

All locators are externalized in JSON files using the **LocatorManager**.

```mermaid
sequenceDiagram
    participant Test as Test Spec
    participant LM as LocatorManager
    participant File as JSON Files

    Test->>LM: load("login")
    LM->>File: Read global.json
    File-->>LM: Global locators
    LM->>File: Read web/common.json
    File-->>LM: Web locators
    LM->>File: Read web/login.json
    File-->>LM: Page locators
    LM-->>Test: Merged Locator Cache Ready

    Test->>Test: findElement("username_field")
    Test->>LM: resolve("username_field")
    LM-->>Test: "#login-user"
```

**Locator Loading Order:**

1. `global.json` - Common across all modes.
2. `{mode}/common.json` - Mode-specific common locators.
3. `{mode}/{page}.json` - Page/feature-specific locators.

### 3. Configuration Management

The **ConfigManager** provides centralized access to validated environment variables:

```python
from src.config.config_manager import config_manager

# Type-safe access with Pydantic validation
browser = config_manager.get('browser')
timeout = config_manager.get('timeout')
```

### 4. Test Execution Flow

```mermaid
sequenceDiagram
    participant Suite as Pytest
    participant Conf as conftest.py
    participant CM as ConfigManager
    participant DF as DriverFactory
    participant Strat as Strategy
    participant Test as Spec

    Suite->>Conf: Request driver fixture
    Conf->>CM: Load AppConfig (reads .env)
    CM-->>Conf: AppConfig object
    Conf->>Conf: Check EXECUTION_MODE
    Conf->>DF: DriverFactory.create(config)
    DF-->>Conf: Strategy Instance (Web/API/Mobile)
    Conf->>Strat: initialize(config)
    Strat-->>Conf: Ready
    Conf->>Test: Execute test(driver)
    Test->>Strat: perform actions (e.g. navigate_to)
    Strat-->>Test: Returns state/elements
    Test-->>Conf: Test Complete
    Conf->>Strat: terminate()
    Suite->>Suite: Finalize Reports
```

## Technology Stack

| Category | Technologies |
|----------|-------------|
| **Core Framework** | Python 3.10+, Pydantic, Pytest |
| **Web Testing** | Playwright, Chromium/Firefox/WebKit |
| **BDD Testing** | Gherkin, pytest-bdd |
| **API Testing** | Playwright (Hybrid) · HTTPX (Specialized) |
| **Mobile Testing** | Appium |
| **Unit Testing** | Pytest |
| **Database** | SQLAlchemy, psycopg2, PyMySQL |
| **Reporting** | Allure, Playwright HTML |

## Extensibility Points

TAFLEX PY is designed for extension at multiple levels:

### 1. Custom Driver Strategies
Simply extend the `UiDriver` or `ApiClient` base classes and register it in the `DriverFactory`.

### 2. Custom Element Wrappers
Extend or create new element wrappers to support unique platform interactions while maintaining a consistent API.

### 3. Fixtures
Customize Playwright fixtures in `conftest.py` to inject global setup/teardown logic or custom dependencies.
