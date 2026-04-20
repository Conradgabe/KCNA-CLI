from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone

from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static

from kcna.config import DURATION_SEC
from kcna.models import Question
from kcna.sampling import sample_exam
from kcna.scoring import grade
from kcna.tui.widgets.question_card import QuestionCard
from kcna.tui.widgets.timer_bar import TimerBar

ALLOWED_KEYS = {"a", "b", "c", "d", "e"}


class ExamScreen(Screen):
    BINDINGS: list = []

    def __init__(self, seed: int | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._seed = seed
        self._questions: list[Question] = []
        self._answers: dict[str, str | None] = {}
        self._index: int = 0
        self._started_at: datetime | None = None
        self._started_mono: float = 0.0
        self._per_q_start: float = 0.0
        self._per_q_times: dict[str, float] = {}
        self._timer_handle = None
        self._session_id: str = uuid.uuid4().hex[:8]

    def compose(self) -> ComposeResult:
        yield TimerBar(id="exam-header")
        yield Vertical(id="exam-card")
        yield Static("", id="exam-footer")

    def on_mount(self) -> None:
        pool = self.app.question_pool
        self._questions = sample_exam(pool, seed=self._seed)
        self._answers = {q.id: None for q in self._questions}
        self._started_at = datetime.now(timezone.utc)
        self._started_mono = time.monotonic()
        self._per_q_start = self._started_mono
        self._render_current()
        self._timer_handle = self.set_interval(1.0, self._tick)

    def _tick(self) -> None:
        elapsed = time.monotonic() - self._started_mono
        remaining = int(DURATION_SEC - elapsed)
        timer = self.query_one(TimerBar)
        timer.remaining = max(0, remaining)
        if remaining <= 0:
            self._finish(timed_out=True)

    def _render_current(self) -> None:
        container = self.query_one("#exam-card", Vertical)
        container.remove_children()
        if self._index >= len(self._questions):
            self._finish(timed_out=False)
            return
        q = self._questions[self._index]
        container.mount(QuestionCard(q))
        footer = self.query_one("#exam-footer", Static)
        footer.update(
            f"Question {self._index + 1} / {len(self._questions)}  \u00b7  "
            f"Press [bold]a[/]/[bold]b[/]/[bold]c[/]/[bold]d[/]"
            + ("/[bold]e[/]" if len(q.options) == 5 else "")
            + " to answer and advance"
        )
        self._per_q_start = time.monotonic()

    def on_key(self, event: events.Key) -> None:
        key = event.key.lower() if event.key else ""
        if self._index >= len(self._questions):
            event.stop()
            event.prevent_default()
            return
        current = self._questions[self._index]
        valid_labels = {opt.label for opt in current.options}
        if key in valid_labels and key in ALLOWED_KEYS:
            self._record_answer(key)
            event.stop()
            event.prevent_default()
            return
        event.stop()
        event.prevent_default()

    def _record_answer(self, label: str) -> None:
        q = self._questions[self._index]
        self._answers[q.id] = label
        self._per_q_times[q.id] = time.monotonic() - self._per_q_start
        self._index += 1
        if self._index >= len(self._questions):
            self._finish(timed_out=False)
        else:
            self._render_current()

    def _finish(self, timed_out: bool) -> None:
        if self._timer_handle is not None:
            self._timer_handle.stop()
            self._timer_handle = None
        finished_at = datetime.now(timezone.utc)
        duration_sec = int(time.monotonic() - self._started_mono)
        result = grade(
            questions=self._questions,
            answers=self._answers,
            started_at=self._started_at,
            finished_at=finished_at,
            duration_sec=duration_sec,
            timed_out=timed_out,
            session_id=self._session_id,
        )
        from kcna.persistence import save_session
        from kcna.tui.screens.results import ResultsScreen

        try:
            save_session(result)
        except OSError:
            pass
        self.app.switch_screen(ResultsScreen(result))
