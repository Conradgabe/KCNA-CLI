from __future__ import annotations

from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from kcna.models import Question
from kcna.tui.widgets.question_card import QuestionCard


class PracticeScreen(Screen):
    BINDINGS = [
        ("n", "next", "Next"),
        ("right", "next", "Next"),
        ("p", "prev", "Previous"),
        ("left", "prev", "Previous"),
        ("q", "app.quit", "Quit"),
    ]

    def __init__(self, questions: list[Question], **kwargs) -> None:
        super().__init__(**kwargs)
        self._questions = questions
        self._i = 0
        self._answers: dict[str, str | None] = {q.id: None for q in questions}
        self._revealed: dict[str, bool] = {q.id: False for q in questions}

    def compose(self) -> ComposeResult:
        yield Vertical(id="practice-body")
        yield Static("", id="practice-footer")

    def on_mount(self) -> None:
        self._refresh_body()

    def _refresh_body(self) -> None:
        body = self.query_one("#practice-body", Vertical)
        body.remove_children()
        if not self._questions:
            body.mount(Static("No questions matched the filter."))
            return
        q = self._questions[self._i]
        body.mount(
            Static(
                f"Practice  \u00b7  Question {self._i + 1} / {len(self._questions)}  "
                f"\u00b7  Domain: {q.domain}",
                classes="result-section",
            )
        )
        body.mount(QuestionCard(q))
        if self._revealed[q.id]:
            chosen = self._answers[q.id]
            correct = q.correct_label()
            if chosen == correct:
                body.mount(
                    Static(
                        f"[green]\u2713 Correct![/]  The answer is "
                        f"[bold]{correct}[/].",
                        classes="practice-feedback-correct",
                    )
                )
            else:
                body.mount(
                    Static(
                        f"[red]\u2717 Wrong.[/]  Your pick: {chosen or '(none)'}.  "
                        f"Correct: [bold]{correct}[/].",
                        classes="practice-feedback-wrong",
                    )
                )
            body.mount(
                Static(
                    f"[bold]Explanation:[/] {q.explanation}",
                    classes="review-explanation",
                )
            )
        footer = self.query_one("#practice-footer", Static)
        if self._revealed[q.id]:
            footer.update(
                "[bold]n[/]/\u2192 next  \u00b7  [bold]p[/]/\u2190 prev  \u00b7  "
                "[bold]q[/] quit"
            )
        else:
            footer.update(
                "Press [bold]a[/]/[bold]b[/]/[bold]c[/]/[bold]d[/]"
                + ("/[bold]e[/]" if len(q.options) == 5 else "")
                + " to answer  \u00b7  [bold]q[/] quit"
            )

    def on_key(self, event: events.Key) -> None:
        if not self._questions:
            return
        key = event.key.lower() if event.key else ""
        q = self._questions[self._i]
        if self._revealed[q.id]:
            return
        valid = {opt.label for opt in q.options}
        if key in valid:
            self._answers[q.id] = key
            self._revealed[q.id] = True
            self._refresh_body()
            event.stop()
            event.prevent_default()

    def action_next(self) -> None:
        if self._i < len(self._questions) - 1:
            self._i += 1
            self._refresh_body()

    def action_prev(self) -> None:
        if self._i > 0:
            self._i -= 1
            self._refresh_body()
