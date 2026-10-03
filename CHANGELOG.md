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
- `hashes/SHA256SUMS` containing checksums for the staged benchmark, runner, launcher, and selected raw result JSONs.

### Evidence state

- Phase-1 result is based on the frozen ZOMAH Laya Primitive Diagnostic v0.8.
- Kev result: 35/36 (97.2%), 0 strong-wrong cases, one borderline miss at `path-002`.
- Lean CPU profile preserved behavior at approximately 1.0 GB resident RAM, ~111-113 ms mean local HTTP latency, and 0.00% sampled idle CPU.
- Canonical artifacts were copied into a publication-staging tree and hashed after copying.
- The configured obvious-secret/local-path scan returned no matches for the staged benchmark, runner, launcher, or selected result JSONs.
- `hashes/KNOWN_HASHES.md` now records the exact staged artifact checksums.

### Pending public audit / publication

- Verify the staged raw artifacts are visible in Google Drive through the provider API.
- Perform final manual content/licensing review of the staged raw files.
- Publish the exact benchmark JSON, SystemOne runner, and selected raw result JSONs.
- Compare the published lean launcher byte-for-byte against the staged canonical copy.
- Recheck README/result summary against the published raw artifacts before the `v0.1.0` freeze.

Canonical local experiment files are not rewritten in place for release.
