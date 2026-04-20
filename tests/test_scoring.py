from datetime import datetime, timezone

from kcna.scoring import failed_questions, grade
from tests.conftest import make_pool


def _grade(pool, answers, timed_out=False):
    start = datetime(2026, 4, 20, 10, 0, tzinfo=timezone.utc)
    end = datetime(2026, 4, 20, 10, 30, tzinfo=timezone.utc)
    return grade(
        questions=pool,
        answers=answers,
        started_at=start,
        finished_at=end,
        duration_sec=1800,
        timed_out=timed_out,
        session_id="test",
    )


def test_all_correct_is_pass():
    pool = make_pool()[:65]
    answers = {q.id: q.correct_label() for q in pool}
    r = _grade(pool, answers)
    assert r.correct == 65
    assert r.score == 1.0
    assert r.passed is True


def test_exactly_48_correct_fails():
    pool = make_pool()[:65]
    answers = {q.id: (q.correct_label() if i < 48 else "a") for i, q in enumerate(pool)}
    for q in pool:
        if not answers[q.id]:
            answers[q.id] = "a"
    r = _grade(pool, answers)
    assert r.correct == 48
    assert r.passed is False


def test_exactly_49_correct_passes():
    pool = make_pool()[:65]
    answers = {}
    for i, q in enumerate(pool):
        answers[q.id] = q.correct_label() if i < 49 else "a"
    r = _grade(pool, answers)
    assert r.correct == 49
    assert r.passed is True


def test_unanswered_counts_as_wrong():
    pool = make_pool()[:65]
    answers = {q.id: None for q in pool}
    r = _grade(pool, answers, timed_out=True)
    assert r.correct == 0
    assert r.passed is False


def test_failed_questions_returns_wrong_only():
    pool = make_pool()[:3]
    answers = {
        pool[0].id: pool[0].correct_label(),
        pool[1].id: "a",
        pool[2].id: None,
    }
    r = _grade(pool, answers)
    wrong = failed_questions(r)
    assert {q.id for q in wrong} == {pool[1].id, pool[2].id}
