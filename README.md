# kcna

A Windows-native CLI simulator for the CNCF **Kubernetes and Cloud Native Associate (KCNA)** certification exam.

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Use

```bash
kcna exam                                 # 65 questions, 90 minutes, 75% to pass
kcna practice --count 20                  # untimed, immediate feedback
kcna practice --domain kubernetes-fundamentals
kcna stats                                # past attempts
kcna stats show <session-id>              # per-domain breakdown
```

## Exam rules (matches the real KCNA sitting style)

- 65 questions drawn from a pool of ~320
- Sampled by the real curriculum weights: 44% Kubernetes Fundamentals, 28% Container Orchestration, 16% Cloud Native Application Delivery, 12% Cloud Native Architecture (incl. Observability)
- 90-minute hard timer; unanswered questions score as wrong at timeout
- **Forward-only** — press `a`/`b`/`c`/`d`/`e` to lock your answer; next question appears immediately
- 75% pass mark (≥ 49/65 correct)

## License

MIT. Seeded questions credit: moabukar/Kubernetes-and-Cloud-Native-Associate-KCNA (Apache-2.0) — see `LICENSES/moabukar-NOTICE.txt`.
