# kcna

A local, terminal-based simulator for the CNCF **Kubernetes and Cloud Native Associate (KCNA)** certification exam. Built in Python with a Textual TUI.

- 65 questions / 90 minutes / 75% to pass
- 304 hand-authored questions across all four current curriculum domains
- Sampled at real exam weights (44 / 28 / 16 / 12)
- Forward-only timed exam mode, untimed practice mode, session history, and a review screen for past attempts

## Requirements

- Python **3.11 or newer** (tested on 3.14)
- Windows, macOS, or Linux terminal that supports modern TUIs (Windows Terminal, iTerm2, Alacritty, Kitty, most native Linux terminals)

## Setup from a fresh clone

```bash
git clone https://github.com/Conradgabe/KCNA-CLI.git
cd KCNA-CLI
```

Create a virtual environment and install the package in editable mode.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

**Windows (cmd.exe):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -e ".[dev]"
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

After activation the `kcna` command is on your PATH. Verify:

```bash
kcna version
kcna --help
```

Run your first exam:

```bash
kcna exam
```

## Commands

| Command | What it does |
|---|---|
| `kcna exam` | Launch a full 65-question, 90-minute timed exam. |
| `kcna practice` | Untimed study mode with immediate feedback after each answer. |
| `kcna review [SESSION_ID]` | Reopen the interactive review screen for a past session. Defaults to `latest`. |
| `kcna stats list` | Table of past exam attempts, newest first. |
| `kcna stats show <SESSION_ID>` | Per-domain breakdown of a specific past attempt. |
| `kcna version` | Print the installed version. |
| `kcna --help` | List all commands. Add `--help` to any subcommand for its flags. |

### `kcna exam` options

```
kcna exam [--seed N] [--bank PATH]
```

- `--seed N` — deterministic sampling seed (useful for reproducibility / tests).
- `--bank PATH` — point at a different directory of question JSON files.

### `kcna practice` options

```
kcna practice [--count N] [--domain D] [--difficulty easy|medium|hard] [--seed N] [--bank PATH]
```

- `--count N` — number of questions (default 20).
- `--domain D` — restrict to one domain. Valid values:
  `kubernetes-fundamentals`, `container-orchestration`,
  `cloud-native-delivery`, `cloud-native-architecture`.
- `--difficulty` — `easy`, `medium`, or `hard`.
- `--seed N` — deterministic sampling.
- `--bank PATH` — alternate question bank directory.

### `kcna review` options

```
kcna review [SESSION_ID]
```

- `SESSION_ID` — the 8-character id shown by `kcna stats list`. Omit or pass `latest` to review your most recent attempt.

## Key bindings

### Title screen
- `Enter` or `s` — start exam
- `q` — quit

### Exam screen (forward-only; no going back)
- `a` / `b` / `c` / `d` / `e` — lock your answer and advance to the next question
- All other keys (Escape, arrows, Backspace, Ctrl+Q) are intentionally ignored

### Practice screen (free navigation)
- `a` / `b` / `c` / `d` / `e` — answer the current question; correct answer and explanation are revealed
- `n` / `→` — next question
- `p` / `←` — previous question
- `q` — quit

### Results screen
- `r` — review wrong answers
- `q` — quit

### Review screen
- `n` / `→` — next failed question
- `p` / `←` — previous failed question
- `q` / `Esc` — exit back to the results screen (or quit the app if invoked via `kcna review`)

## Exam rules

- 65 questions, 90-minute hard timer. Unanswered questions at timeout count as wrong.
- **Forward-only**: once you press an answer key, the answer is locked and the next question appears immediately. There is no review or change during the exam.
- 75% pass mark (at least 49/65 correct).
- Questions are sampled per sitting by real curriculum weights:
  - Kubernetes Fundamentals 44% (29 questions)
  - Container Orchestration 28% (18 questions)
  - Cloud Native Application Delivery 16% (10 questions)
  - Cloud Native Architecture including Observability 12% (8 questions)

## Where data lives

- **Question bank** — ships inside the package at `src/kcna/data/questions/<domain>/*.json`. Each JSON file holds an array of questions sharing a subtopic.
- **Exam history** — each finished attempt is saved as JSON at:
  - Windows: `%LOCALAPPDATA%\kcna\history\`
  - macOS: `~/Library/Application Support/kcna/history/`
  - Linux: `~/.local/share/kcna/history/`

Filenames are `<ISO-timestamp>_<session-id>.json` and contain the sampled questions, your answers, score, per-domain breakdown, and duration.

## Project layout

```
src/kcna/
  cli.py                 # Typer entry point and subcommands
  config.py              # Exam constants (length, duration, pass mark, weights)
  models.py              # Pydantic models (Question, ExamResult, etc.)
  loader.py              # Loads and validates the JSON bank at startup
  validation.py          # Schema rules applied to every question
  sampling.py            # Largest-remainder domain-weighted sampler
  scoring.py             # Grading and per-domain breakdown
  persistence.py         # Save/load past exam sessions
  tui/
    app.py               # Textual App subclasses (Exam, Practice, Review)
    kcna.tcss            # Textual CSS theme
    screens/             # Title, exam, practice, results, review
    widgets/             # Timer bar, question card
  data/questions/        # The shipped question bank
tests/                   # pytest suite (sampling, scoring, validation, loader, persistence, TUI smoke)
LICENSES/                # Attribution for seeded OSS questions
pyproject.toml           # Packaging, dependencies, console-script entry
```

## Running the tests

```bash
pytest -q
```

The suite covers domain-weighted sampling, scoring edges (48/65 fails, 49/65 passes), schema validation, bank loading, session persistence, and Textual Pilot smoke tests of the exam and review screens.

## Adding or editing questions

Each question is JSON in `src/kcna/data/questions/<domain>/<subtopic>.json`:

```json
{
  "id": "kf-ctrl-001",
  "domain": "kubernetes-fundamentals",
  "subtopic": "control-plane",
  "difficulty": "easy",
  "question": "Which component stores cluster state?",
  "options": [
    {"label": "a", "text": "kubelet",    "correct": false},
    {"label": "b", "text": "etcd",       "correct": true},
    {"label": "c", "text": "kube-proxy", "correct": false},
    {"label": "d", "text": "containerd", "correct": false}
  ],
  "explanation": "etcd is the strongly-consistent KV store behind the API server.",
  "references": ["https://kubernetes.io/docs/concepts/overview/components/"]
}
```

Rules enforced at load time:

- `id` unique and matching `^[a-z]{2,4}-[a-z0-9-]+-\d{3}$`
- `domain` one of the four canonical domain ids
- `difficulty` in `easy` / `medium` / `hard`
- 4 or 5 options, labels `a..d` or `a..e` contiguous, exactly one `correct: true`
- File must live under `data/questions/<declared-domain>/`

If any rule fails, the app refuses to start and points at the offending file.

## Contributing

Bug reports, new questions, and corrections are welcome. See
[`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to add or fix questions and the
[`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) for community norms.

To report a security issue privately, see [`SECURITY.md`](./SECURITY.md).

## License

MIT. See [`LICENSE`](./LICENSE).

### A note on question accuracy

Questions were authored against the current public CNCF / Kubernetes
documentation and community best practices. Subject-matter review is ongoing
and corrections are welcome — if you spot a wrong answer or a misleading
explanation, please open an issue using the **Wrong answer** template.
