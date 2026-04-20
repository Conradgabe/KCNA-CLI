import pytest

from kcna.models import Option, Question
from kcna.validation import QuestionValidationError, validate_bank, validate_question


def _make(options, domain="kubernetes-fundamentals", qid="kf-test-001"):
    return Question(
        id=qid,
        domain=domain,
        subtopic="test",
        difficulty="medium",
        question="stem?",
        options=options,
        explanation="x",
    )


def test_rejects_zero_correct():
    q = _make([
        Option(label="a", text="a", correct=False),
        Option(label="b", text="b", correct=False),
        Option(label="c", text="c", correct=False),
        Option(label="d", text="d", correct=False),
    ])
    with pytest.raises(QuestionValidationError):
        validate_question(q)


def test_rejects_two_correct():
    q = _make([
        Option(label="a", text="a", correct=True),
        Option(label="b", text="b", correct=True),
        Option(label="c", text="c", correct=False),
        Option(label="d", text="d", correct=False),
    ])
    with pytest.raises(QuestionValidationError):
        validate_question(q)


def test_rejects_noncontiguous_labels():
    q = _make([
        Option(label="a", text="a", correct=False),
        Option(label="b", text="b", correct=True),
        Option(label="d", text="d", correct=False),
        Option(label="e", text="e", correct=False),
    ])
    with pytest.raises(QuestionValidationError):
        validate_question(q)


def test_rejects_bad_id():
    q = _make([
        Option(label="a", text="a", correct=False),
        Option(label="b", text="b", correct=True),
        Option(label="c", text="c", correct=False),
        Option(label="d", text="d", correct=False),
    ], qid="BADID")
    with pytest.raises(QuestionValidationError):
        validate_question(q)


def test_rejects_duplicate_ids():
    opts = [
        Option(label="a", text="a", correct=False),
        Option(label="b", text="b", correct=True),
        Option(label="c", text="c", correct=False),
        Option(label="d", text="d", correct=False),
    ]
    q1 = _make(opts, qid="kf-test-001")
    q2 = _make(opts, qid="kf-test-001")
    with pytest.raises(QuestionValidationError):
        validate_bank([q1, q2])


def test_accepts_valid_question():
    q = _make([
        Option(label="a", text="a", correct=False),
        Option(label="b", text="b", correct=True),
        Option(label="c", text="c", correct=False),
        Option(label="d", text="d", correct=False),
    ])
    validate_question(q)
