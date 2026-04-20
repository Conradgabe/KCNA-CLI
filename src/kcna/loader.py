from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

from pydantic import ValidationError

from kcna.models import Question
from kcna.validation import QuestionValidationError, validate_bank, validate_question


def _package_questions_root() -> Path:
    pkg = resources.files("kcna") / "data" / "questions"
    return Path(str(pkg))


def load_bank(root: Path | None = None) -> list[Question]:
    root = root or _package_questions_root()
    if not root.exists():
        raise FileNotFoundError(f"question bank not found at {root}")

    questions: list[Question] = []
    json_files = sorted(root.rglob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"no JSON question files found under {root}")

    for path in json_files:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise QuestionValidationError(f"{path}: invalid JSON ({e})") from e

        if not isinstance(raw, list):
            raise QuestionValidationError(
                f"{path}: expected a JSON array of questions"
            )

        for item in raw:
            try:
                q = Question.model_validate(item)
            except ValidationError as e:
                raise QuestionValidationError(f"{path}: {e}") from e
            validate_question(q, source=path)
            questions.append(q)

    validate_bank(questions)
    return questions
