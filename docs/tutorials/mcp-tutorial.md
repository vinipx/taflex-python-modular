# MCP Support Tutorial

In this tutorial, you will learn how to leverage the **Model Context Protocol (MCP)** server embedded in TAFLEX PY to build, run, and debug tests entirely through an AI Assistant like Cursor or Claude Desktop.

---

## Prerequisites

1. You have a virtual environment with the `taflex-py[mcp]` dependency installed.
2. You have configured your AI client (Cursor, Claude Desktop, etc.) with the `taflex-mcp` server. (See [Setup & Configuration](../guides/mcp-integration.md) if you haven't done this yet).

---

## Scenario: AI-Assisted Test Creation and Execution

Imagine you have been tasked with adding a new API test to verify that an endpoint returns correct user data. Instead of writing the code manually, running the test, and debugging failures in your terminal, you will ask the AI to do the heavy lifting using the MCP Server.

### Step 1: Requesting a Scaffold

In your AI chat interface, ask the agent to scaffold a new test suite. The AI will use the `scaffold_test_suite` tool to generate the base file.

**Prompt to AI:**
> *"Please scaffold a new 'api' test suite for the feature 'User Data'. Ensure it is saved in the correct location."*

**What happens:**
The AI invokes the `scaffold_test_suite` tool with arguments `suite_type="api"` and `feature_name="User Data"`. The MCP server creates the file `tests/api/test_user_data.py` containing the TAFLEX PY boilerplate.

### Step 2: Learning Framework Best Practices

Before asking the AI to write the actual test logic, you can ask it to read the framework documentation to ensure it uses the correct API implementation strategy.

**Prompt to AI:**
> *"Now, read the framework documentation resource `docs://guides/api-testing` to understand how we do specialized API testing."*

**What happens:**
The AI requests the `docs://guides/api-testing` resource. It will read that TAFLEX uses a specialized `api_driver` fixture leveraging `httpx` or `playwright`.

### Step 3: Writing the Test

Now, ask the AI to write the test using the knowledge it just gained.

**Prompt to AI:**
> *"Update `tests/api/test_user_data.py`. Write a test that uses the `api_driver` fixture to make a GET request to `/users/1`. Assert the status code is 200 and the response JSON contains a key 'id' equal to 1. Use the `write_test_file` tool."*

**What happens:**
The AI generates the Python code and uses the `write_test_file` tool to overwrite the file contents, ensuring it adheres to the guidelines.

### Step 4: Configuring the Environment

Let's ensure the framework is configured correctly for this test. We can ask the AI to verify the current configuration and update it if necessary.

**Prompt to AI:**
> *"Check the current framework configuration schema and state. Ensure `API_PROVIDER` is set to `httpx`. If not, update the `.env` file using the `update_environment_config` tool."*

**What happens:**
1. The AI reads `config://schema` to understand valid configuration keys.
2. It reads `config://current` to check the current `api_provider` value.
3. If it is not `httpx`, it uses the `update_environment_config` tool to set `API_PROVIDER=httpx`.

### Step 5: Running and Debugging

This is where the magic happens. The AI can run the test itself and diagnose any issues.

**Prompt to AI:**
> *"Run pytest on `tests/api/test_user_data.py` using the `run_pytest` tool. Analyze the output."*

**What happens:**
The AI triggers the `run_pytest` tool. The MCP server spawns a subprocess, executes Pytest, and returns the STDOUT/STDERR. 

**If the test fails** (e.g., due to an incorrect URL or assertion mismatch):
The AI reads the traceback from the output, explains the root cause to you in the chat, and can automatically use `write_test_file` to fix the code and rerun `run_pytest` until it passes!

---

## Summary

By using the MCP server, your AI Assistant has effectively become a pairing partner with direct access to your local test framework. It can:

1. **Scaffold files**
2. **Read documentation to understand context**
3. **Write and format code**
4. **Modify framework configurations**
5. **Execute tests and autonomously iterate on failures**

This workflow drastically reduces context switching, allowing you to stay focused on high-level architecture while the AI handles the repetitive execution loops.