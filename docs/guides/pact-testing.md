# Pact Contract Testing

Pact is a consumer-driven contract testing tool that ensures different services (e.g., a frontend and an API) can communicate correctly.

:::tip Tutorial
Ready to get started? Check out our [**Step-by-Step Contract Testing Tutorial**](../tutorials/contract-testing.md).
:::

## Why Contract Testing?

In a microservices architecture, traditional E2E tests are often slow, flaky, and hard to maintain. Contract testing allows you to:
- **Decouple Teams**: Develop and test services independently.
- **Fast Feedback**: Catch breaking API changes at build time.
- **Reduce Flakiness**: Replace unstable E2E tests with fast, deterministic contract tests.

---

## 🛠 Configuration

Enable Pact in your `.env` file:

```bash
# Enable Pact
PACT_ENABLED=true

# Consumer & Provider Names
PACT_CONSUMER=my-web-app
PACT_PROVIDER=my-api-service

# Pact Broker (Optional)
PACT_BROKER_URL=https://your-pact-broker.com
PACT_BROKER_TOKEN=your-token
```

---

## 🧑‍💻 Consumer Testing Tutorial

Consumer tests define the expectations for how the provider should behave.

### 1. Create a Consumer Test
Create a file in `tests/contract/consumer/test_user.py`:

```python
import requests
from src.core.contracts.pact_manager import pact_manager

def test_user_api_contract():
    pact = pact_manager.setup()
    
    (pact_manager
     .given('user with ID 1 exists')
     .upon_receiving('a request for user 1')
     .with_request('GET', '/users/1')
     .will_respond_with(200, body={"id": 1, "name": "John Doe"}))
     
    def run_test(mock_url):
        response = requests.get(f"{mock_url}/users/1")
        assert response.status_code == 200
        assert response.json()['name'] == 'John Doe'
        
    pact_manager.execute_test(run_test)
```

### 2. Generate the Pact File
Run the tests to generate the JSON contract in the `/pacts` directory.

---

## 🏗 Provider Verification

Provider verification ensures that the real API service actually respects the contracts defined by the consumers.

### 1. Verification Script
Create a script (e.g., `pact_verify.py`) that uses the Pact Verifier:

```python
from pact import Verifier
import os

verifier = Verifier(
    provider='my-api-service',
    provider_base_url='http://localhost:3000'
)

verifier.verify_with_broker(
    broker_url=os.getenv('PACT_BROKER_URL'),
    broker_token=os.getenv('PACT_BROKER_TOKEN'),
    publish_version='1.0.0',
    publish_verification_results=True
)
```

---

## 🚀 CLI Commands

To keep contract tests isolated, run the following commands:

| Command | Description |
| :--- | :--- |
| `pytest tests/contract/consumer` | Run consumer-side contract tests. |
| `# Custom script using pact-cli` | Publish generated pacts to the Broker. |
| `python pact_verify.py` | Run provider-side verification. |
