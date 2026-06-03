"""Health check engine for repositories."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional


@dataclass
class CheckResult:
    """Result of a single health check."""

    check_id: str
    name: str
    description: str
    passed: bool
    suggestion: str = ""
    details: str = ""


def check_license(repo_path: Path) -> CheckResult:
    """Check if the repository has a LICENSE file."""
    license_names = ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md"]
    found = None
    for name in license_names:
        if (repo_path / name).exists():
            found = name
            break

    if found:
        content = (repo_path / found).read_text(encoding="utf-8", errors="ignore")[:2000]
        license_type = "Unknown"
        for ltype in ["Apache-2.0", "MIT", "GPL-3.0", "BSD-3-Clause", "BSD-2-Clause"]:
            if ltype.lower() in content.lower() or ltype in content:
                license_type = ltype
                break
            if ltype == "MIT" and "MIT License" in content:
                license_type = "MIT"
                break
            if ltype == "Apache-2.0" and "Apache License" in content:
                license_type = "Apache-2.0"
                break

        return CheckResult(
            check_id="license",
            name="LICENSE file",
            description=f"LICENSE file exists ({found}, {license_type})",
            passed=True,
            details=f"Detected license: {license_type}",
        )

    return CheckResult(
        check_id="license",
        name="LICENSE file",
        description="LICENSE file is missing",
        passed=False,
        suggestion="Add a LICENSE file. Apache-2.0 or MIT are recommended for open source.",
    )


def check_readme(repo_path: Path) -> CheckResult:
    """Check if the repository has a README file."""
    readme_names = ["README.md", "README.rst", "README.txt", "README"]
    found = None
    for name in readme_names:
        if (repo_path / name).exists():
            found = name
            break

    if not found:
        return CheckResult(
            check_id="readme",
            name="README file",
            description="README file is missing",
            passed=False,
            suggestion="Add a README.md with project description, installation, and usage.",
        )

    content = (repo_path / found).read_text(encoding="utf-8", errors="ignore")
    quality_score = 0
    max_score = 6
    missing = []

    if content.strip().startswith("#"):
        quality_score += 1
    else:
        missing.append("title (h1 heading)")

    if "install" in content.lower():
        quality_score += 1
    else:
        missing.append("installation instructions")

    if "usage" in content.lower() or "
