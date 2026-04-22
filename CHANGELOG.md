# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `kcna review [SESSION_ID]` command to reopen the interactive review screen
  for any past exam session (defaults to the most recent attempt).
- Regression test covering the full exam → results → review flow via Textual
  Pilot.
- Top-level `LICENSE` file (MIT).
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`.
- Issue templates (bug report, wrong answer, feature request) and a PR template.

### Changed
- Documentation: README now includes clone-to-run setup instructions for
  PowerShell, cmd.exe, and POSIX shells, a full commands table, per-screen key
  bindings, data-location notes for all three platforms, and a question
  authoring guide.

### Fixed
- `ReviewScreen` and `PracticeScreen` no longer crash on render. The internal
  refresh helper was renamed from `_render` to `_refresh_body` so it no longer
  shadows Textual's `Widget._render`.
- `kcna review` no longer lands on a blank screen when pressing `q`. The
  review screen now exits the app if it is the only pushed screen, or pops
  back to the results screen if launched inside the full exam flow.

### Removed
- Misleading `LICENSES/moabukar-NOTICE.txt`. All questions in the current bank
  were authored from scratch rather than seeded from that repository, so the
  attribution did not apply.

## [0.1.0] - 2026-04-20

### Added
- Initial release of the KCNA practice exam CLI.
- Textual TUI with `kcna exam`, `kcna practice`, and `kcna stats` subcommands.
- 304 authored questions across the four current curriculum domains, sampled
  per exam at real-exam weights (44 / 28 / 16 / 12).
- Forward-only exam screen with single-keypress advance and hard 90-minute
  timer.
- Domain-weighted sampling via largest-remainder rounding, scoring, per-domain
  breakdown, and pass/fail at 75%.
- Session persistence to the platform-appropriate user data directory.
