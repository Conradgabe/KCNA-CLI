from __future__ import annotations

from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from kcna.config import DOMAIN_LABELS, PASS_MARK
from kcna.models import ExamResult


class ResultsScreen(Screen):
    BINDINGS = [
        ("r", "review", "Review wrong answers"),
        ("q", "app.quit", "Quit"),
    ]

    def __init__(self, result: ExamResult, **kwargs) -> None:
        super().__init__(**kwargs)
        self._result = result

    def compose(self) -> ComposeResult:
        r = self._result
        banner_class = "result-banner-pass" if r.passed else "result-banner-fail"
        banner_text = "PASS" if r.passed else "FAIL"
        with Vertical():
            yield Static(banner_text, classes=banner_class)
            yield Static(
                f"Score: {r.correct} / {r.total}  ({r.score * 100:.1f}%)  \u00b7  "
                f"pass mark {int(PASS_MARK * 100)}%",
                classes="result-section",
            )
            if r.timed_out:
                yield Static(
                    "[yellow]Time expired before all questions were answered. "
                    "Unanswered questions count as wrong.[/]",
                    classes="result-section",
                )
            yield Static(self._render_domain_table(), classes="result-section")
            yield Static(
                f"Duration: {r.duration_sec // 60}m {r.duration_sec % 60}s  \u00b7  "
                f"Session id: {r.session_id}",
                classes="result-section",
            )
            yield Static(
                "[bold]r[/] review wrong answers  \u00b7  [bold]q[/] quit",
                classes="result-section",
            )

    def _render_domain_table(self) -> Table:
        table = Table(title="Per-domain breakdown", show_lines=False)
        table.add_column("Domain")
        table.add_column("Score", justify="right")
        table.add_column("Percent", justify="right")
        for d, (correct, total) in self._result.per_domain.items():
            pct = (correct / total * 100) if total else 0.0
            table.add_row(
                DOMAIN_LABELS.get(d, d),
                f"{correct} / {total}",
                f"{pct:.0f}%",
            )
        return table

    def action_review(self) -> None:
        from kcna.scoring import failed_questions
        from kcna.tui.screens.review import ReviewScreen

        wrong = failed_questions(self._result)
        if not wrong:
            return
        self.app.push_screen(ReviewScreen(self._result, wrong))
