# AI-Agent Integration (MCP)

TAFLEX PY supports the **Model Context Protocol (MCP)**, an open standard that enables AI agents (like Claude Desktop, IDE assistants, and autonomous agents) to interact directly with the testing framework.

By exposing the framework as an MCP server, you transform your test suite from a passive set of files into an active service that AI can explore, execute, and debug.

---

## 🚀 Key Benefits

- **Autonomous Debugging**: AI agents can read test failures, inspect the relevant source code and locators, and attempt to fix the issue by running specific tests to verify the fix.
- **Natural Language Discovery**: Ask your AI assistant "Which tests cover the login flow?" or "Show me the locators for the dashboard," and get immediate, accurate answers.
- **Zero Context Switching**: Run tests and view reports directly within your AI-powered IDE or chat interface without leaving your workflow.
- **Agent-Ready Architecture**: Future-proof your testing strategy by providing a standardized interface for the next generation of AI developers.

---

## 🛠️ Capabilities

The MCP server exposes the following **Tools** and **Resources** to connected AI agents:

### Tools (Actions)
- **`list_specs`**: Scans the project and returns all available `.py` and `.feature` files.
- **`list_locators`**: Lists available locator JSON files by mode (web/mobile).
- **`get_locator`**: Retrieves the content of a specific locator file for inspection.
- **`run_test`**: Triggers a Playwright execution for a specific file and returns the full STDOUT/STDERR.

### Resources (Data)
- **`taflex://config/current`**: The resolved framework configuration (with secrets like API keys automatically masked).
- **`taflex://reports/latest`**: A machine-readable JSON summary of the most recent test execution.

---

## ⚖️ Pros and Cons

### Pros
- **Efficiency**: Drastically reduces the time spent copy-pasting logs and file contents into LLMs.
- **Precision**: Agents get the exact state of the framework and locators, reducing "hallucinations."
- **Standardization**: Uses the industry-standard Model Context Protocol.

### Cons
- **Security**: Since the server can execute shell commands (`pytest`), it should only be used in trusted local environments or with strict permission controls.
- **Statefulness**: Tests may depend on environmental state (databases, clean browser sessions) which the agent must be aware of.

---

## 📖 Use Cases

### 1. The "Fix-It" Loop
When a test fails in CI, a developer can point an AI agent to the failure. The agent uses `taflex://reports/latest` to see the error, `get_locator` to check if a selector changed, and `run_test` to verify a potential fix.

### 2. Test Coverage Audit
Ask an agent: *"Compare our login spec with the locators in login.json. Are we missing any elements in our tests?"* The agent can fetch both resources and provide a gap analysis.

### 3. Onboarding
A new engineer can ask the IDE agent: *"How do I run the API tests for the user service?"* The agent can list the specs, show the configuration, and even run a sample test for them.

---

## ⚙️ Setup & Configuration

To enable AI agents to use TAFLEX PY, you must configure your MCP client to point to the framework's MCP server.

### 1. Identify the Server Path
The MCP server is located at: `src/mcp/server.py` within your project root. You will need the **absolute path** to this file.

### 2. Configure Your Client

#### Claude Desktop
Add the following entry to your `claude_desktop_config.json` (typically located in `%APPDATA%/Claude/` on Windows or `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "taflex": {
      "command": "python",
      "args": ["/absolute/path/to/taflex-python-modular/src/mcp/server.py"],
      "env": {
        "NODE_ENV": "development"
      }
    }
  }
}
```

#### Gemini CLI
You can add the server via the command line:

```bash
gemini mcp add taflex python /absolute/path/to/taflex-python-modular/src/mcp/server.py
```

Alternatively, add it manually to your `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "taflex": {
      "command": "python",
      "args": ["/absolute/path/to/taflex-python-modular/src/mcp/server.py"]
    }
  }
}
```

#### Cursor
1. Go to **Settings > Features > MCP**.
2. Click **+ Add New MCP Server**.
3. Name: `taflex`
4. Type: `command`
5. Command: `python /absolute/path/to/taflex-python-modular/src/mcp/server.py`

#### VS Code (Cline / Roo Code)
If you are using extensions like **Cline** or **Roo Code**:
1. Open the extension settings or the MCP configuration file (usually found in the extension's global storage).
2. Add the server definition:

```json
{
  "mcpServers": {
    "taflex": {
      "command": "python",
      "args": ["/absolute/path/to/taflex-python-modular/src/mcp/server.py"]
    }
  }
}
```

#### OpenCode
Add to your `opencode.json` (global in `~/.config/opencode/` or per-project):

```json
{
  "mcpServers": {
    "taflex": {
      "type": "local",
      "command": "python",
      "args": ["/absolute/path/to/taflex-python-modular/src/mcp/server.py"],
      "enabled": true
    }
  }
}
```

#### GitHub Copilot
GitHub Copilot does not natively support MCP servers at this time. To use TAFLEX MCP with Copilot, you may need a bridge extension or an IDE that integrates both (like Cursor).

### 3. Verify Connection
1. Restart your AI client or refresh the MCP server list.
2. You should see `taflex` listed with tools like `run_test`, `list_specs`, and `get_locator`.
