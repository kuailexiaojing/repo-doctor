"""CLI entry point for repo-doctor."""

from pathlib import Path
from typing import Optional

import click

from .checker import run_checks
from .fixer import run_fix
from .reporter import format_report
from . import __version__


@click.group()
@click.version_option(version=__version__, prog_name="repo-doctor")
def main() -> None:
    """🩺 repo-doctor — Open source repository health diagnostic CLI."""
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False), default=".")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format.",
)
@click.option(
    "--checks",
    type=str,
    default=None,
    help="Comma-separated list of check IDs to run. Run all if not specified.",
)
def check(path: str, output_format: str, checks: Optional[str]) -> None:
    """Run health checks on a repository."""
    repo_path = Path(path).resolve()

    if not (repo_path / ".git").exists():
        click.echo(f"Warning: {repo_path} does not appear to be a git repository.")
        click.echo("   Some checks may not work correctly.\n")

    check_ids = None
    if checks:
        check_ids = [c.strip() for c in checks.split(",")]

    results = run_checks(repo_path, check_ids=check_ids)
    output = format_report(results, repo_path, output_format)
    click.echo(output)


@main.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False), default=".")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompts.")
def fix(path: str, yes: bool) -> None:
    """Auto-fix common issues by generating missing template files."""
    repo_path = Path(path).resolve()
    results = run_checks(repo_path)
    run_fix(results, repo_path, dry_run=not yes)


@main.command(name="ai-suggest")
@click.argument("path", type=click.Path(exists=True, file_okay=False), default=".")
def ai_suggest(path: str) -> None:
    """Generate AI-powered fix suggestions (requires OPENAI_API_KEY)."""
    import os

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY environment variable is not set.")
        click.echo("   Set it with: export OPENAI_API_KEY='your-key-here'")
        raise SystemExit(1)

    repo_path = Path(path).resolve()
    results = run_checks(repo_path)
    failed = [r for r in results if not r.passed]

    if not failed:
        click.echo("All checks passed! No suggestions needed.")
        return

    click.echo(f"Generating AI suggestions for {len(failed)} issues...\n")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        for result in failed:
            prompt = (
                f"You are an open-source repository expert. "
                f"The check '{result.check_id}' failed for a repository. "
                f"Description: {result.description}. "
                f"Suggestion: {result.suggestion}. "
                f"Provide a specific, actionable fix in 2-3 sentences."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            suggestion = response.choices[0].message.content or "No suggestion available."
            click.echo(f"[FAIL] {result.check_id}: {result.description}")
            click.echo(f"   AI Suggestion: {suggestion}\n")

    except ImportError:
        click.echo("Error: openai package not installed.")
        click.echo("   Install it with: pip install repo-doctor[ai]")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
