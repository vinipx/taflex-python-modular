# Contract Testing Tutorial

This tutorial will walk you through creating your first Consumer-Driven Contract test using Pact in **taflex-python-modular**. 

We will simulate a scenario where a **User Web App** (Consumer) expects a specific response from a **User Profile Service** (Provider).

---

## Prerequisites

1.  Ensure you have run `./setup.sh`.
2.  Enable Pact in your `.env`:
    ```env
    PACT_ENABLED=true
    ```

---

## Step 1: Create the Consumer Test

The Consumer defines the "Contract". We want to ensure that when we call `GET /users/profile`, we receive a JSON with `username` and `role`.

Create `tests/contract/consumer/test_profile.py`:

```python
import requests
from src.core.contracts.pact_manager import pact_manager

def test_user_profile_contract():
    pact_manager.setup('user-web-app', 'profile-service')
    
    (pact_manager
     .given('user exists')
     .upon_receiving('a request for user profile')
     .with_request('GET', '/profile')
     .will_respond_with(200, headers={'Content-Type': 'application/json'}, body={
         "username": "johndoe",
         "role": "editor"
     }))
     
    def run_test(mock_url):
        response = requests.get(f"{mock_url}/profile")
        assert response.status_code == 200
        assert response.json()['username'] == 'johndoe'
        
    pact_manager.execute_test(run_test)
```

---

## Step 2: Run the Test and Generate the Pact

Execute the contract test suite:

```bash
pytest tests/contract/consumer
```

**What happened?**
- A mock server was started.
- The test made a real HTTP call to that mock server.
- Pact verified that the call matched the interaction we defined.
- A JSON file was created in the `/pacts` directory. This is your **Contract**.

---

## Step 3: Provider Verification (Conceptual)

Now that you have the JSON contract, the **Provider** team (API developers) must verify that their real service follows it.

1.  Start your local API service (e.g., on `http://localhost:3000`).
2.  Run the verification command:
    ```bash
    python pact_verify.py
    ```

> **Tip**: In a real CI/CD pipeline, you would publish the JSON file to a **Pact Broker** (like PactFlow) and have the Provider pipeline fetch it automatically.

---

## Summary

You have successfully:
1.  Defined a contract as a Consumer.
2.  Verified the contract against a Mock Server.
3.  Generated a portable JSON Pact file.

For more advanced configurations and Pact Broker integration, check the [Pact Testing Guide](../guides/pact-testing.md).
