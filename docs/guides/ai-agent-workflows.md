# AI Agent Workflows & CI/CD Integration

TAFLEX PY's native Model Context Protocol (MCP) server enables not just local debugging, but fully autonomous AI workflows. By providing a standardized interface (Resources and Tools), you can integrate AI agents into your daily development cycle and your CI/CD pipelines.

This guide covers how to set up AI agents locally using various clients (Gemini CLI, Cursor, Claude Code) and how to deploy an autonomous testing agent in GitHub Actions.

---

## 1. Local AI Agent Integration

You can connect your local workspace to an AI Assistant, allowing it to read your framework configuration, debug failing tests, and write code.

### Connecting to Gemini CLI
Gemini CLI has built-in support for MCP servers. You can add the TAFLEX MCP server dynamically or via a configuration file.

**Option A: CLI Setup**
Run this from your project root to register the server:
```bash
gemini mcp add taflex-mcp "taflex-mcp" --trust
```

**Option B: Manual Setup**
Create a `.gemini/settings.json` file in your workspace:
```json
{
  "mcpServers": {
    "taflex-mcp": {
      "command": "taflex-mcp",
      "args": [],
      "trust": true
    }
  }
}
```

**Usage in Gemini CLI:**
- Type `/mcp` in the interactive prompt to verify the connection and see available tools.
- Ask: *"Use the `taflex-mcp` tools to run the web test suite. If any tests fail, analyze the output and fix the locator in the corresponding test file."*

### Connecting to IDEs (Cursor / Roo Code)
In **Cursor** or VS Code extensions like **Roo Code (Cline)**:
1. Go to MCP Settings.
2. Add a new `command` server.
3. Provide the absolute path to the executable: `/absolute/path/to/.venv/bin/taflex-mcp`

### Connecting to Claude Desktop / Claude Code
Edit your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "taflex-mcp": {
      "command": "/absolute/path/to/project/.venv/bin/taflex-mcp",
      "args": []
    }
  }
}
```

---

## 2. Autonomous GitHub Actions Agent

The true power of MCP is realized when deployed in CI/CD. You can create a GitHub Workflow that triggers an AI agent to autonomously investigate and fix failing tests when a PR is opened or a nightly run fails.

### Architecture
1. **The Trigger:** A GitHub Action is triggered (e.g., via `issue_comment` when a user types `/fix-tests`).
2. **The MCP Server:** The action installs `taflex-py[mcp]` and exposes the framework's capabilities.
3. **The Agent:** A lightweight Python script (using LangChain or Anthropic SDK) connects to the MCP server.
4. **The Loop:** The agent runs Pytest, reads the failing code, rewrites the file, and runs Pytest again.
5. **The Commit:** Once the test passes, the action commits the fix back to the branch.

### Example: The GitHub Workflow
Create `.github/workflows/ai-agent.yml`:

```yaml
name: Autonomous Test Maintainer

on:
  issue_comment:
    types: [created]

jobs:
  fix-tests:
    # Trigger only if someone comments "/fix-tests" on a PR
    if: github.event.issue.pull_request && contains(github.event.comment.body, '/fix-tests')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.ref }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Framework and AI Dependencies
        run: |
          pip install -e ".[all]"
          playwright install --with-deps
          # Install your preferred AI SDK here (e.g., anthropic, mcp)
          pip install anthropic mcp

      - name: Run AI Debugging Agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        # Assuming you have a script that initializes an Anthropic client with the MCP server
        run: python scripts/ci_agent.py

      - name: Commit and Push Fixes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add tests/ src/
          git diff --staged --quiet || (git commit -m "test: AI autonomously fixed test failures" && git push)
          
      - name: React to Comment
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.reactions.createForIssueComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              comment_id: context.payload.comment.id,
              content: "rocket"
            });
```

### Example: The Agent Script (`scripts/ci_agent.py`)
*Note: This is a conceptual representation of how an agent uses the MCP client to loop through tools.*

```python
import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # 1. Connect to the local Taflex MCP Server
    server_params = StdioServerParameters(
        command="taflex-mcp",
        args=[]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 2. Instruct the AI (Conceptual API Call to LLM)
            prompt = """
            You are an autonomous test engineer. 
            Use the 'run_pytest' tool. 
            If it fails, use 'read_project_file' to understand the code, 
            'write_test_file' to fix it, and run pytest again.
            Stop when 'run_pytest' returns Exit Code 0.
            """
            
            # 3. The LLM Client library would loop here, requesting tool calls
            # from the session and returning the results to the LLM.
            print("Agent loop initiated...")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Practical Use Cases

Here are examples of prompts you can use with your connected AI Agent to maximize productivity:

### The "Self-Healing" Run
> "Run the entire test suite using the `run_pytest` tool. For every failure you encounter, read the traceback, inspect the relevant Page Object in the `src/` folder, fix the selector, and re-run the test until the suite is green."

### The "Context-Aware" Scaffold
> "I need to write a BDD test for a new 'Shopping Cart' feature. Please read `docs://guides/bdd-testing` to understand how TAFLEX handles Gherkin. Then, scaffold the `.feature` file and the corresponding step definition Python file in the `tests/bdd/` directory."

### The Code Quality Enforcer
> "Find all files in `tests/web/` that were modified recently. Use the `format_code` tool to run Ruff on them and ensure they comply with our strict typing and formatting standards."