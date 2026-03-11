import pytest
import shutil

from taflex.mcp_server import _safe_resolve, _backup_file, PROJECT_ROOT, MCP_DIR

def test_safe_resolve_allowed_path():
    """Test that safe_resolve works for allowed paths like 'tests/'."""
    # Should resolve correctly within tests/
    target = _safe_resolve("tests/dummy_test.py")
    assert target == (PROJECT_ROOT / "tests/dummy_test.py").resolve()

    # Should resolve correctly within src/
    target_src = _safe_resolve("src/dummy_src.py")
    assert target_src == (PROJECT_ROOT / "src/dummy_src.py").resolve()

def test_safe_resolve_directory_traversal():
    """Test that directory traversal outside of allowed boundaries raises ValueError."""
    # Attempt to access something completely outside PROJECT_ROOT
    with pytest.raises(ValueError, match="Security Error: Path traversal detected.|Security Error: Access restricted"):
        _safe_resolve("../../../etc/passwd")

    # Attempt to access root files not in allowed dirs (e.g., .env) when not explicitly allowed
    with pytest.raises(ValueError, match="Security Error: Access restricted"):
         _safe_resolve(".env", allowed_dirs=["tests", "src"])

def test_backup_file(tmp_path):
    """Test that the backup mechanism correctly creates a backup copy."""
    # Create a dummy file to back up
    dummy_file = PROJECT_ROOT / "tests/dummy_to_backup.py"
    dummy_file.parent.mkdir(parents=True, exist_ok=True)
    dummy_file.write_text("print('hello')", encoding="utf-8")

    try:
        _backup_file(dummy_file)
        
        # Check if backup was created
        backup_dir = MCP_DIR / "backups"
        assert backup_dir.exists()
        
        # Find backups of this file
        backups = list(backup_dir.glob("dummy_to_backup.py.*.bak"))
        assert len(backups) > 0
        assert "print('hello')" in backups[0].read_text(encoding="utf-8")
    finally:
        # Cleanup
        if dummy_file.exists():
            dummy_file.unlink()
        if MCP_DIR.exists():
            shutil.rmtree(MCP_DIR)
