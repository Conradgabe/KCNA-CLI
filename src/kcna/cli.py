from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from kcna import __version__
from kcna.config import DOMAIN_LABELS, PASS_MARK

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="KCNA practice exam CLI.",
)

stats_app = typer.Typer(help="Inspect past exam sessions.")
app.add_typer(stats_app, name="stats")

console = Console()


@app.command()
def exam(
    seed: int | None = typer.Option(None, help="Deterministic sampling seed."),
    bank: Path | None = typer.Option(None, help="Override question bank directory."),
) -> None:
    """Launch a full 65-question, 90-minute timed exam."""
    from kcna.tui.app import ExamApp

    ExamApp(bank_path=bank, seed=seed).run()


@app.command()
def practice(
    count: int = typer.Option(20, min=1, help="How many questions to drill."),
    domain: str | None = typer.Option(None, help="Filter to a single domain id."),
    difficulty: str | None = typer.Option(
        None, help="Filter to easy|medium|hard."
    ),
    seed: int | None = typer.Option(None, help="Deterministic sampling seed."),
    bank: Path | None = typer.Option(None, help="Override question bank directory."),
) -> None:
    """Untimed study mode with immediate feedback."""
    from kcna.tui.app import PracticeApp

    PracticeApp(
        bank_path=bank,
        count=count,
        domain=domain,
        difficulty=difficulty,
        seed=seed,
    ).run()


@app.command()
def review(
    session_id: str = typer.Argument(
        "latest",
        help="Session id to review, or 'latest' for the most recent attempt.",
    ),
) -> None:
    """Reopen the interactive review screen for a past exam session."""
    from kcna.models import ExamResult
    from kcna.persistence import list_sessions, load_session
    from kcna.scoring import failed_questions
    from kcna.tui.app import ReviewApp

    if session_id == "latest":
        sessions = list_sessions()
        if not sessions:
            typer.echo("No saved sessions yet. Run `kcna exam` first.")
            raise typer.Exit(code=1)
        result = ExamResult.model_validate_json(
            sessions[0].read_text(encoding="utf-8")
        )
    else:
        result = load_session(session_id)
        if result is None:
            typer.echo(f"No session with id {session_id}")
            raise typer.Exit(code=1)

    wrong = failed_questions(result)
    if not wrong:
        typer.echo(
            f"Session {result.session_id} has no wrong answers to review "
            f"({result.correct}/{result.total})."
        )
        return

    ReviewApp(result).run()


@app.command("version")
def version_cmd() -> None:
    """Print the installed kcna version."""
    typer.echo(__version__)


@stats_app.command("list")
def stats_list() -> None:
    """List past exam sessions newest-first."""
    from kcna.models import ExamResult
    from kcna.persistence import list_sessions

    sessions = list_sessions()
    if not sessions:
        typer.echo("No saved sessions yet. Run `kcna exam` to create one.")
        return

    table = Table(title="Exam History")
    table.add_column("Session id")
    table.add_column("Started")
    table.add_column("Score", justify="right")
    table.add_column("Pct", justify="right")
    table.add_column("Result")
    table.add_column("Duration")

    for p in sessions:
        try:
            r = ExamResult.model_validate_json(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        table.add_row(
            r.session_id,
            r.started_at.strftime("%Y-%m-%d %H:%M"),
            f"{r.correct} / {r.total}",
            f"{r.score * 100:.1f}%",
            "[green]PASS[/]" if r.passed else "[red]FAIL[/]",
            f"{r.duration_sec // 60}m {r.duration_sec % 60}s",
        )
    console.print(table)


@stats_app.command("show")
def stats_show(session_id: str) -> None:
    """Print per-domain breakdown of a past session."""
    from kcna.persistence import load_session

    r = load_session(session_id)
    if r is None:
        typer.echo(f"No session with id {session_id}")
        raise typer.Exit(code=1)

    banner = "[bold green]PASS[/]" if r.passed else "[bold red]FAIL[/]"
    console.print(
        f"\nSession {r.session_id}  \u00b7  {r.started_at.isoformat()}  \u00b7  {banner}"
    )
    console.print(
        f"Score: {r.correct} / {r.total}  ({r.score * 100:.1f}%)  \u00b7  "
        f"pass mark {int(PASS_MARK * 100)}%"
    )
    if r.timed_out:
        console.print("[yellow]Note: exam timed out before completion.[/]")

    t = Table(title="Per-domain")
    t.add_column("Domain")
    t.add_column("Score", justify="right")
    t.add_column("Pct", justify="right")
    for d, (c, total) in r.per_domain.items():
        pct = (c / total * 100) if total else 0.0
        t.add_row(DOMAIN_LABELS.get(d, d), f"{c} / {total}", f"{pct:.0f}%")
    console.print(t)
