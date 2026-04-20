from __future__ import annotations

from textual.reactive import reactive
from textual.widgets import Static

from kcna.config import DURATION_SEC, WARN_RED_SEC, WARN_YELLOW_SEC


def format_mmss(seconds: int) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


class TimerBar(Static):
    remaining: reactive[int] = reactive(DURATION_SEC)

    def render(self) -> str:
        mmss = format_mmss(self.remaining)
        if self.remaining <= WARN_RED_SEC:
            color = "red"
        elif self.remaining <= WARN_YELLOW_SEC:
            color = "yellow"
        else:
            color = "green"
        return f"[bold {color}] Time remaining: {mmss} [/]"
