"""Tests for the checker module."""

import pytest
from pathlib import Path

from repo_doctor.checker import (
    run_checks,
    check_license,
    check_readme,
    check_contributing,
    check_changelog,
    check_gitignore,
    check_ci,
    check_code_style,
    check_security_gitignore,
)


@pytest.fixture
def minimal_repo(tmp_path: Path) -> Path:
    """Create a minimal repo with just .git directory."""
    (tmp_path / ".git").mkdir()
    return tmp_path


@pytest.fixture
def healthy_repo(tmp_path: Path) -> Path:
    """Create a repo that passes most checks."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "LICENSE").write_text("Apache License\nVersion 2.0\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "# My Project\n\nA test project.\n\n## Installation\n\npip install my-project\n\n## Usage\n\n
