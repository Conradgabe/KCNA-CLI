from __future__ import annotations

EXAM_LEN = 65
DURATION_SEC = 90 * 60
PASS_MARK = 0.75

DOMAIN_WEIGHTS: dict[str, float] = {
    "kubernetes-fundamentals": 0.44,
    "container-orchestration": 0.28,
    "cloud-native-delivery": 0.16,
    "cloud-native-architecture": 0.12,
}

DOMAIN_LABELS: dict[str, str] = {
    "kubernetes-fundamentals": "Kubernetes Fundamentals",
    "container-orchestration": "Container Orchestration",
    "cloud-native-delivery": "Cloud Native Application Delivery",
    "cloud-native-architecture": "Cloud Native Architecture",
}

DIFFICULTIES = ("easy", "medium", "hard")

WARN_YELLOW_SEC = 10 * 60
WARN_RED_SEC = 60
