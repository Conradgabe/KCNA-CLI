from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from kcna.config import DURATION_SEC, EXAM_LEN, PASS_MARK


class TitleScreen(Screen):
    BINDINGS = [
        ("enter", "start", "Start exam"),
        ("s", "start", "Start exam"),
        ("q", "app.quit", "Quit"),
    ]

    def __init__(self, bank_size: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self._bank_size = bank_size

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("KCNA Practice Exam", id="title-banner")
            yield Static(
                f"{EXAM_LEN} questions  \u00b7  "
                f"{DURATION_SEC // 60} minutes  \u00b7  "
                f"{int(PASS_MARK * 100)}% to pass",
                classes="title-info",
            )
            yield Static(
                f"Question bank: {self._bank_size} questions",
                classes="title-info",
            )
            yield Static(
                "Press [bold green]Enter[/] or [bold green]s[/] to start  \u00b7  "
                "[bold red]q[/] to quit",
                id="title-start-hint",
            )

    def action_start(self) -> None:
        from kcna.tui.screens.exam import ExamScreen

        self.app.push_screen(ExamScreen())
