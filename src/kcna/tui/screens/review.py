from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from kcna.config import DOMAIN_LABELS
from kcna.models import ExamResult, Question


class ReviewScreen(Screen):
    BINDINGS = [
        ("n", "next", "Next"),
        ("right", "next", "Next"),
        ("p", "prev", "Previous"),
        ("left", "prev", "Previous"),
        ("q", "pop", "Back"),
        ("escape", "pop", "Back"),
    ]

    def __init__(self, result: ExamResult, wrong: list[Question], **kwargs) -> None:
        super().__init__(**kwargs)
        self._result = result
        self._wrong = wrong
        self._i = 0

    def compose(self) -> ComposeResult:
        yield Vertical(id="review-body")

    def on_mount(self) -> None:
        self._render()

    def _render(self) -> None:
        body = self.query_one("#review-body", Vertical)
        body.remove_children()
        if not self._wrong:
            body.mount(Static("No wrong answers to review."))
            return
        q = self._wrong[self._i]
        user_pick = self._result.answers.get(q.id)
        correct_label = q.correct_label()
        domain = DOMAIN_LABELS.get(q.domain, q.domain)

        body.mount(
            Static(
                f"Failed {self._i + 1} / {len(self._wrong)}  \u00b7  "
                f"Domain: {domain}  \u00b7  "
                f"Your pick: {user_pick or '(unanswered)'}  \u00b7  "
                f"Correct: {correct_label}",
                classes="result-section",
            )
        )
        body.mount(Static(q.question, classes="result-section"))
        for opt in q.options:
            if opt.label == correct_label:
                text = f"[green]\u2713 ({opt.label}) {opt.text}[/]"
                cls = "review-option-correct"
            elif opt.label == user_pick:
                text = f"[red]\u2717 ({opt.label}) {opt.text}[/]"
                cls = "review-option-wrong"
            else:
                text = f"  ({opt.label}) {opt.text}"
                cls = "review-option-normal"
            body.mount(Static(text, classes=cls))

        body.mount(
            Static(
                f"[bold]Explanation:[/] {q.explanation}",
                classes="review-explanation",
            )
        )
        body.mount(
            Static(
                "[bold]n[/]/\u2192 next  \u00b7  [bold]p[/]/\u2190 prev  \u00b7  "
                "[bold]q[/] back",
                classes="result-section",
            )
        )

    def action_next(self) -> None:
        if self._i < len(self._wrong) - 1:
            self._i += 1
            self._render()

    def action_prev(self) -> None:
        if self._i > 0:
            self._i -= 1
            self._render()

    def action_pop(self) -> None:
        self.app.pop_screen()
