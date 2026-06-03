"""Report formatting for check results."""

import json
from dataclasses import asdict
from pathlib import Path

from .checker import CheckResult


def calculate_health_score(results: list[CheckResult]) -> int:
    """Calculate a 0-100 health score based on check results."""
    if not results:
        return 0

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    score = int((passed / total) * 100)
    return score


def format_report_text(results: list[CheckResult], repo_path: Path) -> str:
    """Format check results as human-readable text."""
    lines = []
    lines.append("repo-doctor Diagnostic Report")
    lines.append("=" * 40)
    lines.append(f"Project: {repo_path.name}")
    lines.append(f"Path: {repo_path}")
    lines.append("")

    categories = {
        "Key Files": ["license", "readme", "contributing", "changelog", "gitignore"],
        "CI/CD & Code Style": ["ci", "code_style"],
        "Security": ["security_gitignore"],
    }

    for category_name, check_ids in categories.items():
        lines.append(f"[{category_name}]")
        for result in results:
            if result.check_id in check_ids:
                icon = "PASS" if result.passed else "FAIL"
                lines.append(f"  [{icon}] {result.name} - {result.description}")
                if result.suggestion and not result.passed:
                    lines.append(f"       Suggestion: {result.suggestion}")
        lines.append("")

    uncategorized_ids = set()
    for ids in categories.values():
        uncategorized_ids.update(ids)
    uncategorized = [r for r in results if r.check_id not in uncategorized_ids]
    if uncategorized:
        lines.append("[Other Checks]")
        for result in uncategorized:
            icon = "PASS" if result.passed else "FAIL"
            lines.append(f"  [{icon}] {result.name} - {result.description}")
        lines.append("")

    score = calculate_health_score(results)
    lines.append(f"Health Score: {score}/100")
    lines.append("")

    failed = [r for r in results if not r.passed]
    if failed:
        lines.append("Fix Suggestions:")
        for i, result in enumerate(failed, 1):
            lines.append(f"  {i}. {result.suggestion or result.description}")

    return "\n".join(lines)


def format_report_json(results: list[CheckResult], repo_path: Path) -> str:
    """Format check results as JSON."""
    score = calculate_health_score(results)
    data = {
        "repository": str(repo_path),
        "name": repo_path.name,
        "health_score": score,
        "total_checks": len(results),
        "passed_checks": sum(1 for r in results if r.passed),
        "failed_checks": sum(1 for r in results if not r.passed),
        "results": [asdict(r) for r in results],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_report(results: list[CheckResult], repo_path: Path, output_format: str = "text") -> str:
    """Format check results in the specified format."""
    if output_format == "json":
        return format_report_json(results, repo_path)
    return format_report_text(results, repo_path)
