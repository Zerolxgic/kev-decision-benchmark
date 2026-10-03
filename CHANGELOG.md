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
- `hashes/SHA256SUMS` containing checksums for the frozen benchmark, runner, launcher, and selected raw result JSONs.
- Exact raw Phase-1 result JSONs for the initial Kev CPU run, three repeats, and two lean-profile runs.

### Evidence state

- Phase-1 result is based on the frozen ZOMAH Laya Primitive Diagnostic v0.8.
- Kev result: 35/36 (97.2%), 0 strong-wrong cases, one borderline miss at `path-002`.
- Lean CPU profile preserved behavior at approximately 1.0 GB resident RAM, ~111-113 ms mean local HTTP latency, and 0.00% sampled idle CPU.
- Canonical artifacts were copied into a publication-staging tree and hashed after copying.
- The configured obvious-secret/local-path scan returned no matches for the staged benchmark, runner, launcher, or selected result JSONs.
- Manual publication review found no credentials, private identities, or private machine paths in the Phase-1 raw artifacts.
- All nine frozen public artifacts passed SHA-256 verification before the evidence commit.
- Phase-1 evidence boundary commit: `d5e53ebb40ecf1815c459844175c1e4764650754` (`Add frozen Kev phase-1 evidence`).
- GitHub remote inspection confirmed the raw evidence commit is present and exposes the expected Kev run data.

### Release state

Phase-1 evidence publication is complete. The remaining `v0.1.0` action is to tag the final release-documentation state. No further changes to the frozen Phase-1 evidence set are expected.

Canonical local experiment files were not rewritten in place for release.
