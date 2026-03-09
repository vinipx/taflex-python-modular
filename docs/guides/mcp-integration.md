# AI-Agent Integration (MCP)

TAFLEX PY natively supports the **Model Context Protocol (MCP)**, an open standard that enables AI agents (such as Claude Desktop, Cursor, and autonomous CI/CD agents) to interact directly with the testing framework.

By implementing an MCP server using the official `mcp` Python SDK, TAFLEX PY transforms your test suite from a passive repository of code into an active, intelligent service. AI agents can introspect the framework configuration, securely read and write test files, and autonomously execute Pytest to debug failures.

---

## 🚀 Key Benefits

- **Autonomous Debugging**: AI agents can read test failures directly from `pytest` execution, inspect the source code, and fix issues by running tests repeatedly until they pass.
- **Dynamic Context**: Rather than guessing environment variables or framework syntax, agents pull the exact Pydantic `AppConfig` JSON schema and framework documentation dynamically.
- **Safe Execution Boundaries**: The server strictly limits reads and writes to the `src/` and `tests/` directories, ensuring agents cannot manipulate core system files or leak credentials.
- **Zero Context Switching**: Run tests, inspect locators, and view traces directly within your AI-powered IDE without switching to the terminal.

---

## 🏗️ Architecture

The TAFLEX MCP implementation (`src/taflex/mcp_server.py`) acts as a bridge between the AI client and your local testing environment over STDIO. It leverages **FastMCP** to expose Resources (context) and Tools (actions).

### Resources (Context & State)
Resources provide static and dynamic information to the AI agent to help it understand the framework.

- **`config://schema`**: Returns the `AppConfig.model_json_schema()`, instantly teaching the agent what environment variables exist, their types, and default values.
- **`config://current`**: Returns the active configuration state. Sensitive variables (like `xray_client_secret` or API keys) are automatically masked (`********`) to prevent context leakage.
- **`docs://{doc_name}`**: Allows the agent to read framework documentation (e.g., `docs://best-practices/test-design`) to learn TAFLEX conventions before generating code.

### Tools (Actions)
Tools empower the AI agent to perform read/write operations and execute tests.

- **`update_environment_config(key, value)`**: Safely updates or creates variables in the `.env` file to quickly change browsers, execution modes, or base URLs.
- **`run_pytest(test_path, marker)`**: Triggers a Pytest run in a subprocess with a strict timeout. It returns the raw `stdout`/`stderr` allowing the agent to parse tracebacks and fix broken tests.
- **`list_test_files(directory)`**: Globs the repository for `test_*.py` files, allowing the agent to discover existing tests safely.
- **`read_test_file(relative_path)` & `write_test_file(relative_path, content)`**: Enables the agent to read source/test code and create or update tests. These tools enforce directory jailing (only paths under `tests/` or `src/` are allowed).
- **`scaffold_test_suite(suite_type, feature_name)`**: Rapidly generates boilerplate test code properly marked with `@pytest.mark.{suite_type}`.

---

## ⚙️ Setup & Configuration

To enable AI agents to use the TAFLEX PY server, you must configure your MCP client (IDE or Assistant) to point to the `taflex-mcp` executable.

### 1. Ensure Dependencies are Installed
First, ensure that the MCP dependencies are installed in your virtual environment:

```bash
# Install with the mcp extra
pip install -e ".[mcp]"
```

This registers the `taflex-mcp` CLI command within your virtual environment (`.venv/bin/taflex-mcp`).

### 2. Configure Your AI Client

#### Cursor IDE (Recommended)
1. Go to **Cursor Settings > Features > MCP**.
2. Click **+ Add New MCP Server**.
3. **Name**: `taflex-py`
4. **Type**: `command`
5. **Command**: Provide the absolute path to the executable inside your virtual environment. 
   - *Example (Mac/Linux)*: `/path/to/your/project/.venv/bin/taflex-mcp`
   - *Example (Windows)*: `C:\path\to\your\project\.venv\Scripts\taflex-mcp.exe`

#### Claude Desktop
Add the following entry to your `claude_desktop_config.json` (typically located in `%APPDATA%/Claude/` on Windows or `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "taflex-py": {
      "command": "/absolute/path/to/your/project/.venv/bin/taflex-mcp",
      "args": []
    }
  }
}
```

#### Roo Code / Cline (VS Code Extensions)
1. Open the extension's MCP configuration settings.
2. Add the server definition:

```json
{
  "mcpServers": {
    "taflex-py": {
      "command": "/absolute/path/to/your/project/.venv/bin/taflex-mcp",
      "args": []
    }
  }
}
```

### 3. Verify Connection
Once configured, restart your AI client or refresh the server list. You should now see the `taflex-py` server and have access to all the tools and resources mentioned above!

---

## 📖 Practical Use Cases

Here are a few ways to interact with your AI agent once the MCP server is connected:

**"Fix my failing tests"**
> "Please run the pytest suite for `tests/web/test_login.py`. If it fails, read the file, fix the broken locator based on the current JSON, and run it again until it passes."

**"Change the execution environment"**
> "Update the environment configuration to run tests in headed mode using Firefox instead of Chromium."

**"Scaffold new coverage"**
> "Scaffold a new API test suite for 'User Profiles'. Read `docs://guides/api-testing` first to understand the framework's API strategy. Then, write a test that verifies a GET request to `/users/profile` returns a 200 status."

For a step-by-step example, check out the [MCP Support Tutorial](../tutorials/mcp-tutorial.md).