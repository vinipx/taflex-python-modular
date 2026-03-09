import json
from unittest.mock import patch, MagicMock

import pytest
pytest.importorskip("mcp", reason="mcp module not found. Skipping MCP tests as it was likely not included in scaffolding.")

from taflex.mcp_server import (
    get_config_schema,
    get_current_config,
    get_framework_docs,
    update_environment_config,
    run_pytest,
    list_test_files,
    read_test_file,
    write_test_file,
    scaffold_test_suite
)
import taflex.mcp_server as mcp_server_module

def test_get_config_schema():
    schema_str = get_config_schema()
    schema = json.loads(schema_str)
    assert "title" in schema
    assert schema["title"] == "AppConfig"

def test_get_current_config():
    config_str = get_current_config()
    config = json.loads(config_str)
    assert "execution_mode" in config

def test_get_framework_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    doc_file = docs_dir / "test-doc.md"
    doc_file.write_text("Test content", encoding="utf-8")
    
    content = get_framework_docs("test-doc")
    assert content == "Test content"
    
    missing_content = get_framework_docs("missing-doc")
    assert "not found" in missing_content

def test_update_environment_config(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    env_file = tmp_path / ".env"
    env_file.write_text("EXISTING_KEY=old_value\n", encoding="utf-8")
    
    result = update_environment_config("NEW_KEY", "new_value")
    assert "Successfully updated" in result
    
    result2 = update_environment_config("EXISTING_KEY", "updated_value")
    assert "Successfully updated" in result2
    
    content = env_file.read_text(encoding="utf-8")
    assert "NEW_KEY=new_value" in content
    assert "EXISTING_KEY=updated_value" in content

@patch("subprocess.run")
def test_run_pytest(mock_run, tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "pytest passed"
    mock_result.stderr = ""
    mock_run.return_value = mock_result
    
    result = run_pytest("tests/dummy", marker="api")
    
    mock_run.assert_called_once()
    assert "pytest passed" in result
    assert "Exit Code: 0" in result

def test_list_test_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_dummy.py").write_text("pass", encoding="utf-8")
    (tests_dir / "other_file.py").write_text("pass", encoding="utf-8")
    
    result = list_test_files("tests/")
    assert "test_dummy.py" in result
    assert "other_file.py" not in result

def test_read_test_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    target_file = tests_dir / "test_read.py"
    target_file.write_text("def test_foo(): pass", encoding="utf-8")
    
    result = read_test_file("tests/test_read.py")
    assert result == "def test_foo(): pass"
    
    error_result = read_test_file("invalid_dir/test.py")
    assert "Can only read from" in error_result
    
    missing_result = read_test_file("tests/missing.py")
    assert "does not exist" in missing_result

def test_write_test_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    
    result = write_test_file("tests/test_write.py", "def test_bar(): pass")
    assert "Successfully wrote" in result
    
    written_content = (tmp_path / "tests" / "test_write.py").read_text(encoding="utf-8")
    assert written_content == "def test_bar(): pass"
    
    error_result = write_test_file("src/test_write.py", "pass")
    assert "Can only write to" in error_result

def test_scaffold_test_suite(tmp_path, monkeypatch):
    monkeypatch.setattr(mcp_server_module, "PROJECT_ROOT", tmp_path)
    
    result = scaffold_test_suite("api", "My Feature")
    assert "Successfully scaffolded" in result
    
    expected_path = tmp_path / "tests" / "api" / "test_my_feature.py"
    assert expected_path.exists()
    
    content = expected_path.read_text(encoding="utf-8")
    assert "@pytest.mark.api" in content
    assert "def test_my_feature():" in content
    
    # Test invalid suite type
    error_result = scaffold_test_suite("invalid", "Feature")
    assert "Invalid suite_type" in error_result
    
    # Test file already exists
    error_result2 = scaffold_test_suite("api", "My Feature")
    assert "already exists" in error_result2
