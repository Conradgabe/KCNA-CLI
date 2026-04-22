from __future__ import annotations

from pathlib import Path

from textual.app import App

from kcna.loader import load_bank
from kcna.models import ExamResult, Question


class ExamApp(App):
    CSS_PATH = "kcna.tcss"
    TITLE = "KCNA Practice Exam"

    def __init__(self, bank_path: Path | None = None, seed: int | None = None) -> None:
        super().__init__()
        self.question_pool: list[Question] = load_bank(bank_path)
        self.exam_seed = seed

    def on_mount(self) -> None:
        from kcna.tui.screens.title import TitleScreen

        self.push_screen(TitleScreen(bank_size=len(self.question_pool)))


class PracticeApp(App):
    CSS_PATH = "kcna.tcss"
    TITLE = "KCNA Practice"

    def __init__(
        self,
        bank_path: Path | None = None,
        count: int = 20,
        domain: str | None = None,
        difficulty: str | None = None,
        seed: int | None = None,
    ) -> None:
        super().__init__()
        self._pool = load_bank(bank_path)
        self._count = count
        self._domain = domain
        self._difficulty = difficulty
        self._seed = seed

    def on_mount(self) -> None:
        from kcna.sampling import sample_practice
        from kcna.tui.screens.practice import PracticeScreen

        sampled = sample_practice(
            self._pool,
            count=self._count,
            domain=self._domain,
            difficulty=self._difficulty,
            seed=self._seed,
        )
        self.push_screen(PracticeScreen(sampled))


class ReviewApp(App):
    CSS_PATH = "kcna.tcss"
    TITLE = "KCNA Review"

    def __init__(self, result: ExamResult) -> None:
        super().__init__()
        self._result = result

    def on_mount(self) -> None:
        from kcna.scoring import failed_questions
        from kcna.tui.screens.review import ReviewScreen

        wrong = failed_questions(self._result)
        self.push_screen(ReviewScreen(self._result, wrong))
