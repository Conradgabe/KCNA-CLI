from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from kcna.models import Question


class QuestionCard(Vertical):
    DEFAULT_CSS = """
    QuestionCard {
        padding: 1 2;
    }
    QuestionCard > .question-body {
        padding: 1 0;
        color: $text;
    }
    QuestionCard > .option {
        padding: 0 2;
        margin-top: 1;
    }
    """

    def __init__(self, question: Question, **kwargs) -> None:
        super().__init__(**kwargs)
        self._question = question

    def compose(self) -> ComposeResult:
        yield Static(self._question.question, classes="question-body")
        for opt in self._question.options:
            yield Static(
                f"[bold cyan]({opt.label})[/] {opt.text}",
                classes="option",
            )
