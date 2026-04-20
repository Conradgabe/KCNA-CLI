from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Domain = Literal[
    "kubernetes-fundamentals",
    "container-orchestration",
    "cloud-native-delivery",
    "cloud-native-architecture",
]

Difficulty = Literal["easy", "medium", "hard"]


class Option(BaseModel):
    label: str
    text: str
    correct: bool = False


class Question(BaseModel):
    id: str
    domain: Domain
    subtopic: str
    difficulty: Difficulty = "medium"
    question: str
    options: list[Option]
    explanation: str
    references: list[str] = Field(default_factory=list)

    def correct_label(self) -> str:
        for opt in self.options:
            if opt.correct:
                return opt.label
        raise ValueError(f"Question {self.id} has no correct option")


class AnsweredQuestion(BaseModel):
    question_id: str
    chosen_label: str | None
    time_taken_sec: float


class ExamResult(BaseModel):
    session_id: str
    started_at: datetime
    finished_at: datetime
    duration_sec: int
    timed_out: bool
    questions: list[Question]
    answers: dict[str, str | None]
    per_domain: dict[str, tuple[int, int]]
    correct: int
    total: int
    score: float
    passed: bool
