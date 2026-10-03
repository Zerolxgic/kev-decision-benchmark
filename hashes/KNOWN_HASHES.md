# Known hashes and pinned revisions

This file records provenance values used in the initial Kev benchmark phase.

## Frozen benchmark

- File: `primitive-diagnostic-v0.8.json`
- Benchmark: ZOMAH Laya Primitive Diagnostic
- Version: 0.8
- Cases: 36
- SHA-256: `0e974e7e68a069e1615ba82e26d4551868fc16e5ed17b35872c852b9f097b8d4`

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

These values are preserved so later runs can distinguish changes in benchmark data, runner semantics, model artifact, and runtime revision.
