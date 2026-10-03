# Changelog

All notable public benchmark changes will be recorded here.

## 0.1.0 - 2026-10-03

### Added

- Initial public repository scaffolding.
- Split licensing by artifact type:
  - Apache-2.0 for code, scripts, and experiment runners.
  - CC BY 4.0 for benchmark data, documentation, reports, tables, and figures authored for this project.
- Root Apache 2.0 license text plus `LICENSE-CODE`, `LICENSE-CONTENT`, and `LICENSES.md` scope documentation.
- Public README describing the phase-1 Kev evaluation and architecture boundary.
- Collaboration disclosure.
- Evidence and metrics methodology.
- Known benchmark/runtime hashes and pinned llama.cpp revision.
- Phase-1 result summary.
- Initial benchmark report.
- Reproducible lean CPU launcher for `ggml-org/Kev-0.8B-GGUF:Q8_0`.

### Evidence state

- Phase-1 result is based on the frozen ZOMAH Laya Primitive Diagnostic v0.8.
- Kev result: 35/36 (97.2%), 0 strong-wrong cases, one borderline miss at `path-002`.
- Lean CPU profile preserved behavior at approximately 1.0 GB resident RAM, ~111-113 ms mean local HTTP latency, and 0.00% sampled idle CPU.

### Pending public audit

- Exact benchmark JSON.
- SystemOne benchmark runner.
- Raw per-run JSON outputs.
- Any additional machine/runtime logs intended for publication.

Those artifacts will be copied from the canonical lab only after privacy and publication audit. Existing canonical local files are not rewritten for release.
