from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from kcna.config import DOMAIN_WEIGHTS, PASS_MARK
from kcna.models import ExamResult, Question


def grade(
    questions: list[Question],
    answers: dict[str, str | None],
    started_at: datetime,
    finished_at: datetime,
    duration_sec: int,
    timed_out: bool,
    session_id: str,
) -> ExamResult:
    per_domain_correct: dict[str, int] = defaultdict(int)
    per_domain_total: dict[str, int] = defaultdict(int)
    correct = 0

    for q in questions:
        per_domain_total[q.domain] += 1
        chosen = answers.get(q.id)
        if chosen is None:
            continue
        if chosen == q.correct_label():
            correct += 1
            per_domain_correct[q.domain] += 1

    total = len(questions)
    score = correct / total if total else 0.0
    passed = score >= PASS_MARK

    per_domain: dict[str, tuple[int, int]] = {}
    for d in DOMAIN_WEIGHTS:
        per_domain[d] = (per_domain_correct[d], per_domain_total[d])

    return ExamResult(
        session_id=session_id,
        started_at=started_at,
        finished_at=finished_at,
        duration_sec=duration_sec,
        timed_out=timed_out,
        questions=questions,
        answers=answers,
        per_domain=per_domain,
        correct=correct,
        total=total,
        score=score,
        passed=passed,
    )


def failed_questions(result: ExamResult) -> list[Question]:
    wrong: list[Question] = []
    for q in result.questions:
        chosen = result.answers.get(q.id)
        if chosen != q.correct_label():
            wrong.append(q)
    return wrong
