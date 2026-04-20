from __future__ import annotations

import re
from pathlib import Path

from kcna.config import DIFFICULTIES, DOMAIN_WEIGHTS
from kcna.models import Question

ID_PATTERN = re.compile(r"^[a-z]{2,4}-[a-z0-9]+(-[a-z0-9]+)*-\d{3}$")
ALLOWED_LABELS = ("a", "b", "c", "d", "e")


class QuestionValidationError(Exception):
    pass


def validate_question(q: Question, source: Path | None = None) -> None:
    where = f" ({source})" if source else ""

    if not ID_PATTERN.match(q.id):
        raise QuestionValidationError(
            f"id '{q.id}' does not match {ID_PATTERN.pattern}{where}"
        )

    if q.domain not in DOMAIN_WEIGHTS:
        raise QuestionValidationError(
            f"unknown domain '{q.domain}' in {q.id}{where}"
        )

    if q.difficulty not in DIFFICULTIES:
        raise QuestionValidationError(
            f"difficulty '{q.difficulty}' in {q.id} must be one of {DIFFICULTIES}{where}"
        )

    if not q.question.strip():
        raise QuestionValidationError(f"empty question body in {q.id}{where}")

    if not q.explanation.strip():
        raise QuestionValidationError(f"empty explanation in {q.id}{where}")

    if not 4 <= len(q.options) <= 5:
        raise QuestionValidationError(
            f"{q.id} has {len(q.options)} options; must be 4 or 5{where}"
        )

    expected = ALLOWED_LABELS[: len(q.options)]
    labels = tuple(opt.label for opt in q.options)
    if labels != expected:
        raise QuestionValidationError(
            f"{q.id} option labels are {labels}; expected {expected}{where}"
        )

    correct_count = sum(1 for o in q.options if o.correct)
    if correct_count != 1:
        raise QuestionValidationError(
            f"{q.id} has {correct_count} correct options; must be exactly 1{where}"
        )

    for opt in q.options:
        if not opt.text.strip():
            raise QuestionValidationError(
                f"{q.id} option {opt.label} has empty text{where}"
            )

    if source is not None:
        expected_dir = q.domain
        if expected_dir not in str(source.parent).replace("\\", "/"):
            raise QuestionValidationError(
                f"{q.id} declares domain '{q.domain}' but lives at {source}{where}"
            )


def validate_bank(questions: list[Question]) -> None:
    seen: dict[str, Question] = {}
    for q in questions:
        if q.id in seen:
            raise QuestionValidationError(
                f"duplicate id '{q.id}' appears more than once in the question bank"
            )
        seen[q.id] = q
