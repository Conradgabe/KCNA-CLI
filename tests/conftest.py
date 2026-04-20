from __future__ import annotations

from kcna.models import Option, Question


def _mk(qid: str, domain: str, correct_label: str = "b") -> Question:
    opts = []
    for lbl in ["a", "b", "c", "d"]:
        opts.append(
            Option(label=lbl, text=f"option {lbl}", correct=(lbl == correct_label))
        )
    return Question(
        id=qid,
        domain=domain,
        subtopic="test",
        difficulty="medium",
        question=f"stem for {qid}?",
        options=opts,
        explanation="because.",
    )


def make_pool() -> list[Question]:
    pool: list[Question] = []
    for i in range(1, 60):
        pool.append(_mk(f"kf-t-{i:03d}", "kubernetes-fundamentals"))
    for i in range(1, 40):
        pool.append(_mk(f"co-t-{i:03d}", "container-orchestration"))
    for i in range(1, 30):
        pool.append(_mk(f"cnd-t-{i:03d}", "cloud-native-delivery"))
    for i in range(1, 20):
        pool.append(_mk(f"cna-t-{i:03d}", "cloud-native-architecture"))
    return pool
