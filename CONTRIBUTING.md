# Contributing to kcna

Thanks for helping improve this KCNA practice simulator. The most valuable
contributions are **subject-matter fixes to questions** and **new, high-quality
questions** that reflect the current KCNA curriculum.

## Ways to contribute

1. **Fix a wrong answer or misleading explanation.** Open an issue using the
   *Wrong answer* template, or send a PR directly.
2. **Add new questions.** Aim for the same style and difficulty as the existing
   bank. See the schema rules below.
3. **Improve the TUI or tooling.** Bug reports, Textual rendering fixes,
   keyboard bindings, and cross-platform polish are all welcome.

## Local setup

```bash
git clone https://github.com/Conradgabe/KCNA-CLI.git
cd KCNA-CLI
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -e ".[dev]"
```

Run the test suite before opening a PR:

```bash
pytest -q
```

## Adding or editing a question

Questions live under `src/kcna/data/questions/<domain>/<subtopic>.json` and are
validated at load time.

### Schema

```json
{
  "id": "kf-ctrl-026",
  "domain": "kubernetes-fundamentals",
  "subtopic": "control-plane",
  "difficulty": "medium",
  "question": "Question stem...",
  "options": [
    {"label": "a", "text": "...",           "correct": false},
    {"label": "b", "text": "correct one",   "correct": true},
    {"label": "c", "text": "...",           "correct": false},
    {"label": "d", "text": "...",           "correct": false}
  ],
  "explanation": "Why the correct answer is correct; optionally why the others fail.",
  "references": ["https://kubernetes.io/docs/..."]
}
```

### Rules enforced by the loader

- `id` is unique across the bank and matches `^[a-z]{2,4}-[a-z0-9-]+-\d{3}$`.
- `domain` is one of:
  - `kubernetes-fundamentals`
  - `container-orchestration`
  - `cloud-native-delivery`
  - `cloud-native-architecture`
- `difficulty` is `easy`, `medium`, or `hard`.
- `options` has 4 or 5 entries. Labels are contiguous lowercase starting at `a`
  (`a,b,c,d` or `a,b,c,d,e`).
- Exactly one option has `"correct": true`.
- `question`, `explanation`, and every `option.text` are non-empty.
- The file lives under `data/questions/<declared-domain>/`.

### Style guidance

- Prefer short, scenario-first stems (e.g., "A team needs X. Which resource
  fits best?") over pure definition recall when possible.
- Keep options roughly parallel in length and grammar.
- Make the three distractors **plausible** — not obviously wrong.
- Add at least one official `references` URL when the topic has canonical docs.
- Avoid dated claims (specific version numbers, deprecated features) unless the
  question is explicitly about that history.
- No emojis in questions, options, or explanations.

### Running just the bank-level checks

```bash
pytest tests/test_loader.py tests/test_validation.py -q
```

## Commits and PRs

- One logical change per PR.
- Keep commit subject lines short; put the *why* in the body.
- If your PR adds or changes a question, include the reasoning (docs link,
  curriculum alignment) in the PR description so reviewers can verify.

## Filing issues

- **Wrong answer / bad question** → use the *Wrong answer* issue template and
  include the session id (if from an exam), the question id, the options, your
  proposed correct answer, and a source link.
- **Bug** → include the command you ran, expected vs. actual, and your OS +
  Python version (`python --version`).
- **Feature request** → describe the user problem first; an implementation
  suggestion is nice but optional.

Thank you for contributing.
