import subprocess
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from taflex.core.config.app_config import AppConfig

# Initialize FastMCP Server
mcp = FastMCP("TaFlex-MCP-Server")
PROJECT_ROOT = Path(__file__).parent.parent.parent

# ---------------------------------------------------------
# RESOURCES (Context & State)
# ---------------------------------------------------------

@mcp.resource("config://schema")
def get_config_schema() -> str:
    """Provides the JSON schema of the framework's configuration."""
    return json.dumps(AppConfig.model_json_schema(), indent=2)

@mcp.resource("config://current")
def get_current_config() -> str:
    """Provides the active configuration state."""
    config_dict = AppConfig().model_dump()
    # Mask secrets
    for key in ["xray_client_secret", "rp_api_key", "pact_broker_token"]:
        if config_dict.get(key):
            config_dict[key] = "********"
    return json.dumps(config_dict, indent=2)

@mcp.resource("docs://{doc_name}")
def get_framework_docs(doc_name: str) -> str:
    """Dynamically loads framework guidelines to teach the AI how to write tests."""
    # Maps specific AI requests to your /docs folder
    # e.g., docs://best-practices/test-design
    doc_path = PROJECT_ROOT / f"docs/{doc_name}.md"
    if doc_path.exists():
        return doc_path.read_text(encoding="utf-8")
    return f"Documentation {doc_name} not found."

# ---------------------------------------------------------
# TOOLS (Actions)
# ---------------------------------------------------------

@mcp.tool()
def update_environment_config(key: str, value: str) -> str:
    """Updates or adds a configuration key in the root .env file."""
    env_path = PROJECT_ROOT / ".env"
    lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            updated = True
            break
            
    if not updated:
        lines.append(f"{key}={value}")
        
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return f"Successfully updated {key} in .env file."

@mcp.tool()
def run_pytest(test_path: str = "tests/", marker: str = None) -> str:
    """Executes pytest and returns the result for AI analysis."""
    cmd = ["pytest", test_path, "--tb=short"]
    if marker:
        cmd.extend(["-m", marker])
        
    try:
        result = subprocess.run(
            cmd, 
            cwd=PROJECT_ROOT, 
            capture_output=True, 
            text=True, 
            timeout=300 # 5 min timeout
        )
        return f"Exit Code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Test execution timed out after 5 minutes."

@mcp.tool()
def list_test_files(directory: str = "tests/") -> str:
    """Recursively globs and returns all test files in the given directory."""
    dir_path = PROJECT_ROOT / directory
    
    # Simple check, resolve not available easily in a fast way without breaking path resolution in py < 3.9,
    # but we are on py310, let's use is_relative_to
    try:
        if not dir_path.resolve().is_relative_to(PROJECT_ROOT.resolve()) or not dir_path.exists():
            return f"Error: Invalid or non-existent directory {directory}"
    except Exception as e:
        return f"Error reading path: {e}"
        
    test_files = list(dir_path.rglob("test_*.py"))
    return "\n".join([str(p.relative_to(PROJECT_ROOT)) for p in test_files])

@mcp.tool()
def read_test_file(relative_path: str) -> str:
    """Reads an existing test file from the repository."""
    if not (relative_path.startswith("tests/") or relative_path.startswith("src/")):
        return "Error: Can only read from tests/ or src/ directories."
        
    target_path = PROJECT_ROOT / relative_path
    if not target_path.exists():
        return f"Error: File {relative_path} does not exist."
        
    return target_path.read_text(encoding="utf-8")

@mcp.tool()
def write_test_file(relative_path: str, content: str) -> str:
    """Creates or updates a test file in the tests/ directory."""
    if not relative_path.startswith("tests/"):
        return "Error: Can only write to the tests/ directory."
        
    target_path = PROJECT_ROOT / relative_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote test to {relative_path}"

@mcp.tool()
def scaffold_test_suite(suite_type: str, feature_name: str) -> str:
    """Generates boilerplate test code for a new feature suite."""
    valid_types = ["api", "web", "mobile", "bdd"]
    if suite_type not in valid_types:
        return f"Error: Invalid suite_type. Must be one of {valid_types}"
        
    filename = f"test_{feature_name.replace(' ', '_').lower()}.py"
    filepath = PROJECT_ROOT / "tests" / suite_type / filename
    
    if filepath.exists():
        return f"Error: File already exists at {filepath.relative_to(PROJECT_ROOT)}"
        
    boilerplate = f'import pytest\n\n@pytest.mark.{suite_type}\ndef test_{feature_name.replace(" ", "_").lower()}():\n    """\n    Test case for {feature_name} ({suite_type})\n    """\n    pass\n'
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(boilerplate, encoding="utf-8")
    return f"Successfully scaffolded test suite at {filepath.relative_to(PROJECT_ROOT)}"

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
