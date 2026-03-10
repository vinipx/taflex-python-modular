import subprocess
import json
import logging
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime
from taflex.core.config.app_config import AppConfig

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    FastMCP = None  # Handle graceful exit if MCP is not installed

PROJECT_ROOT = Path(__file__).parent.parent.parent
MCP_DIR = PROJECT_ROOT / ".taflex-mcp"

def setup_logging():
    if not MCP_DIR.exists():
        MCP_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(MCP_DIR / "audit.log"),
            logging.StreamHandler(sys.stderr)
        ]
    )

def _safe_resolve(relative_path: str, allowed_dirs: list[str] = ["tests", "src"]) -> Path:
    target_path = (PROJECT_ROOT / relative_path).resolve()
    
    # 1. Check if it's within PROJECT_ROOT
    if not target_path.is_relative_to(PROJECT_ROOT.resolve()):
        raise ValueError("Security Error: Path traversal detected.")
        
    # 2. Check if it's within an allowed directory
    if not any(target_path.is_relative_to((PROJECT_ROOT / d).resolve()) for d in allowed_dirs):
         raise ValueError(f"Security Error: Access restricted to {allowed_dirs}")
         
    return target_path

def _backup_file(target_path: Path):
    if target_path.exists():
        backup_dir = MCP_DIR / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{target_path.name}.{timestamp}.bak"
        shutil.copy2(target_path, backup_path)
        logging.info(f"Backed up {target_path} to {backup_path}")

if FastMCP:
    mcp = FastMCP("TaFlex-MCP-Server")

    @mcp.resource("config://schema")
    def get_config_schema() -> str:
        """Provides the JSON schema of the framework's configuration."""
        return json.dumps(AppConfig.model_json_schema(), indent=2)

    @mcp.resource("config://current")
    def get_current_config() -> str:
        """Provides the active configuration state."""
        config_dict = AppConfig().model_dump()
        for key in ["xray_client_secret", "rp_api_key", "pact_broker_token"]:
            if config_dict.get(key):
                config_dict[key] = "********"
        return json.dumps(config_dict, indent=2)

    @mcp.resource("docs://{doc_name}")
    def get_framework_docs(doc_name: str) -> str:
        """Dynamically loads framework guidelines to teach the AI how to write tests."""
        try:
            doc_path = PROJECT_ROOT / f"docs/{doc_name}.md"
            if doc_path.exists():
                return doc_path.read_text(encoding="utf-8")
            return f"Documentation {doc_name} not found."
        except Exception as e:
            logging.error(f"Error reading documentation {doc_name}: {e}")
            return f"Error: Unable to read documentation {doc_name}."

    @mcp.tool()
    def update_environment_config(key: str, value: str) -> str:
        """Updates or adds a configuration key in the root .env file."""
        try:
            env_path = PROJECT_ROOT / ".env"
            _backup_file(env_path)
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
            logging.info(f"Updated {key} in .env file.")
            return f"Successfully updated {key} in .env file."
        except Exception as e:
            logging.error(f"Error updating environment config: {e}")
            return f"Error updating config: {e}"

    @mcp.tool()
    def run_pytest(test_path: str = "tests/", marker: str = None) -> str:
        """Executes pytest and returns the result for AI analysis."""
        try:
            target_path = _safe_resolve(test_path, allowed_dirs=["tests", "src"])
            # Use quiet mode and short tracebacks to save context
            cmd = ["pytest", str(target_path), "-q", "--tb=short", "--disable-warnings"]
            
            if marker:
                if not re.match(r"^[a-zA-Z0-9_\-]+$", marker):
                    raise ValueError("Security Error: Invalid marker format.")
                cmd.extend(["-m", marker])
                
            logging.info(f"Agent triggered pytest with path: {test_path}")
            result = subprocess.run(
                cmd, 
                cwd=PROJECT_ROOT, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            stdout_str = result.stdout
            if len(stdout_str) > 4000:
                stdout_str = stdout_str[:4000] + "\n... [TRUNCATED FOR LENGTH] ..."
                
            return f"Exit Code: {result.returncode}\n\nOutput:\n{stdout_str}"
        except subprocess.TimeoutExpired:
            return "Error: Test execution timed out after 5 minutes."
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            logging.error(f"Error running pytest: {e}")
            return f"System Error executing pytest: {e}"

    @mcp.tool()
    def list_project_files(directory: str = ".", pattern: str = "*.py") -> str:
        """Recursively globs and returns allowed files in the given directory."""
        try:
            dir_path = PROJECT_ROOT / directory
            if not dir_path.resolve().is_relative_to(PROJECT_ROOT.resolve()):
                 raise ValueError("Security Error: Path traversal detected.")
            
            allowed = False
            for allowed_dir in ["tests", "src"]:
                if dir_path.resolve().is_relative_to((PROJECT_ROOT / allowed_dir).resolve()) or dir_path.resolve() == PROJECT_ROOT.resolve():
                    allowed = True
                    break
                    
            if not allowed:
                 return "Error: Can only list files in tests/ or src/ directories."

            if not dir_path.exists():
                return f"Error: Directory {directory} does not exist."
            
            files = list(dir_path.rglob(pattern))
            filtered_files = [str(p.relative_to(PROJECT_ROOT)) for p in files if 
                              p.is_relative_to(PROJECT_ROOT / "tests") or p.is_relative_to(PROJECT_ROOT / "src")]
            
            return "\n".join(filtered_files)
        except Exception as e:
            logging.error(f"Error listing files: {e}")
            return f"Error reading path: {e}"

    @mcp.tool()
    def read_project_file(relative_path: str) -> str:
        """Safely reads a file, handling binary or missing files gracefully."""
        try:
            target_path = _safe_resolve(relative_path, allowed_dirs=["tests", "src", "docs"])
            if not target_path.exists():
                return f"Error: File {relative_path} does not exist."
                
            return target_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            logging.warning(f"Agent attempted to read binary file: {relative_path}")
            return "Error: File appears to be binary or non-UTF-8 encoded. Cannot read contents."
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            logging.error(f"Unexpected error reading {relative_path}: {e}")
            return "System Error: Unable to read file due to an internal error."

    @mcp.tool()
    def write_test_file(relative_path: str, content: str) -> str:
        """Creates or updates a test file safely in the tests/ directory."""
        try:
            target_path = _safe_resolve(relative_path, allowed_dirs=["tests"])
            _backup_file(target_path)
            
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")
            logging.info(f"Agent wrote test file to {relative_path}")
            return f"Successfully wrote test to {relative_path}"
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            logging.error(f"Error writing to {relative_path}: {e}")
            return f"Error writing file: {e}"

    @mcp.tool()
    def format_code(relative_path: str) -> str:
        """Runs Ruff format and check --fix on a specific file."""
        try:
            target_path = _safe_resolve(relative_path, allowed_dirs=["tests", "src"])
            if not target_path.exists():
                 return f"Error: File {relative_path} does not exist."
                 
            subprocess.run(["ruff", "check", "--fix", str(target_path)], check=False, capture_output=True)
            subprocess.run(["ruff", "format", str(target_path)], check=False, capture_output=True)
            logging.info(f"Agent formatted {relative_path}")
            return f"Successfully formatted and linted {relative_path}"
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            logging.error(f"Formatting failed for {relative_path}: {e}")
            return f"Formatting failed: {str(e)}"

    @mcp.tool()
    def scaffold_test_suite(suite_type: str, feature_name: str) -> str:
        """Generates boilerplate test code for a new feature suite."""
        valid_types = ["api", "web", "mobile", "bdd"]
        if suite_type not in valid_types:
            return f"Error: Invalid suite_type. Must be one of {valid_types}"
            
        try:
            filename = f"test_{feature_name.replace(' ', '_').lower()}.py"
            relative_path = f"tests/{suite_type}/{filename}"
            target_path = _safe_resolve(relative_path, allowed_dirs=["tests"])
            
            if target_path.exists():
                return f"Error: File already exists at {relative_path}"
                
            boilerplate = f'import pytest\n\n@pytest.mark.{suite_type}\ndef test_{feature_name.replace(" ", "_").lower()}():\n    """\n    Test case for {feature_name} ({suite_type})\n    """\n    pass\n'
            
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(boilerplate, encoding="utf-8")
            logging.info(f"Agent scaffolded test suite at {relative_path}")
            return f"Successfully scaffolded test suite at {relative_path}"
        except ValueError as ve:
            return str(ve)
        except Exception as e:
            logging.error(f"Error scaffolding suite: {e}")
            return f"Error scaffolding suite: {e}"

def main():
    if not FastMCP:
        print("MCP is not installed. To use the AI agent, install taflex-py with the [mcp] extra.", file=sys.stderr)
        sys.exit(1)
        
    setup_logging()
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()