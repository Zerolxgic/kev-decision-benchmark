# Known hashes and pinned revisions

This file records provenance values used in the initial Kev benchmark phase.

## Frozen benchmark

- File: `primitive-diagnostic-v0.8.json`
- Benchmark: ZOMAH Laya Primitive Diagnostic
- Version: 0.8
- Cases: 36
- SHA-256: `0e974e7e68a069e1615ba82e26d4551868fc16e5ed17b35872c852b9f097b8d4`

## SystemOne runner

- File: `run_systemone.py`
- SHA-256: `e5e53275696fb788dac358eda18e2e3f84ea8f2a927af8d88627480a40779205`

## Lean Kev launcher

- File: `start_kev_cpu_lean.sh`
- SHA-256: `504df6cd824321fa9751bb712ea69a547aebd8af261b9aef07d7d5ffc743b5e0`

## Kev result artifacts

- Initial CPU run `run-20261003T110554Z.json`: `4a39004999656387371bb78b7f9d71b0fc01039970f44be57e48b6f1038fdbb5`
- Repeat 1 `run-20261003T110950Z.json`: `40098f1843ac6049ab9764b103ac3941f0e45bccdd85bdb746b1e66e6454a6e9`
- Repeat 2 `run-20261003T110954Z.json`: `5e189541fa1ee78c5737b680d257044368425718592280e3c1673f892f15e02c`
- Repeat 3 `run-20261003T110958Z.json`: `4761274fc2a7ebe5336d03598e8850a6fee0b6f9a217820e2eea68372d4919a5`
- Lean run `run-20261003T112416Z.json`: `02da4bce5f70b260d340f1f2073477fa6366a5db2476b29708b53105b8eb9a1c`
- Lean run `run-20261003T112520Z.json`: `fe21b71bade9f1e73740e396be1dbcd66a7be638ce9fb8977c41e7ea2300ef38`

## Original Laya runner retained for comparison

- File: `run_primitive_diagnostic.py`
- SHA-256: `aa9a1fde8326ddce0d22531b0f0e3a4bd4fee023a13e70c5197d03db3cc77ca5`

## llama.cpp runtime

- Version observed: `0.5.0-dev`
- Build: `11371`
- Commit: `99b95488cac0f00ce3f05af113a8c1e287753f87`
- Commit short form: `99b95488`

## Model identifier

- Kev: `ggml-org/Kev-0.8B-GGUF:Q8_0`

## Publication staging note

The public-staging copies were hashed after copying from the canonical local lab. The publication scan for the staged benchmark, runner, launcher, and result JSONs returned no matches for the configured obvious-secret/local-path patterns. Hashes are preserved before publication so later copies can be verified byte-for-byte.

These values let later runs distinguish changes in benchmark data, runner semantics, model artifact, runtime revision, launcher configuration, and published result files.
