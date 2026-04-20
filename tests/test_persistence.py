from datetime import datetime, timezone

from kcna import persistence as pmod
from kcna.models import ExamResult
from kcna.scoring import grade
from tests.conftest import make_pool


def _dummy_result():
    pool = make_pool()[:3]
    answers = {q.id: q.correct_label() for q in pool}
    return grade(
        questions=pool,
        answers=answers,
        started_at=datetime(2026, 4, 20, 10, 0, tzinfo=timezone.utc),
        finished_at=datetime(2026, 4, 20, 10, 30, tzinfo=timezone.utc),
        duration_sec=1800,
        timed_out=False,
        session_id="abcdef12",
    )


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(pmod, "history_dir", lambda: tmp_path)
    r = _dummy_result()
    out = pmod.save_session(r)
    assert out.exists()
    assert ":" not in out.name
    loaded = pmod.load_session("abcdef12")
    assert isinstance(loaded, ExamResult)
    assert loaded.session_id == "abcdef12"
    assert loaded.correct == 3


def test_list_sessions_newest_first(tmp_path, monkeypatch):
    monkeypatch.setattr(pmod, "history_dir", lambda: tmp_path)
    r = _dummy_result()
    p1 = pmod.save_session(r)
    r2 = r.model_copy(update={"session_id": "fedcba21"})
    p2 = pmod.save_session(r2)
    sessions = pmod.list_sessions()
    assert set(p.name for p in sessions) == {p1.name, p2.name}
