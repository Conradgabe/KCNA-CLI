from __future__ import annotations

from pathlib import Path

from platformdirs import user_data_dir

from kcna.models import ExamResult


def history_dir() -> Path:
    d = Path(user_data_dir("kcna", appauthor=False)) / "history"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _safe_timestamp(dt) -> str:
    return dt.strftime("%Y-%m-%dT%H-%M-%S")


def save_session(result: ExamResult) -> Path:
    d = history_dir()
    fname = f"{_safe_timestamp(result.started_at)}_{result.session_id}.json"
    path = d / fname
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return path


def list_sessions() -> list[Path]:
    d = history_dir()
    return sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)


def load_session(session_id: str) -> ExamResult | None:
    d = history_dir()
    for p in d.glob(f"*_{session_id}.json"):
        return ExamResult.model_validate_json(p.read_text(encoding="utf-8"))
    return None
