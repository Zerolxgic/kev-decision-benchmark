# Kev Decision Benchmark

*Evaluating Kev-0.8B as a small CPU-first local decision model for ZOMAH through llama.cpp's `/v1/systemone` interface.*

## Overview

This repository documents an evaluation of `ggml-org/Kev-0.8B-GGUF:Q8_0` as a local semantic decision component inside the ZOMAH agent-system architecture.

The immediate architectural question is deliberately narrow:

> Can a small decision model stay resident on CPU, make useful semantic judgments quickly enough for orchestration, and leave the RX 7800 XT available for Gemma?

The current result is promising, but preliminary. Kev has not been selected permanently for ZOMAH. The first test phase uses a frozen 36-case benchmark originally created to diagnose Laya, followed by runtime and resource measurements. A broader ZOMAH-specific Decision Benchmark v1 is the next evidence class.

## Collaboration

This benchmark is a human-directed, AI-collaborative research project developed by **Zerrius and ChatGPT**.

Zerrius directs the research, runs the local experiments, controls the execution environment, and makes architecture and publication decisions. ChatGPT assists with experiment design, analysis, failure interpretation, documentation, and synthesis. Experimental claims are grounded in recorded artifacts and observed results rather than AI assistance itself.

See [`docs/COLLABORATION.md`](docs/COLLABORATION.md).

## Current research question

Can Kev-0.8B serve as an always-resident CPU-first decision layer for ZOMAH while deterministic code remains responsible for policy, exact machine facts, validation, and execution?

## Runtime

- Model: `ggml-org/Kev-0.8B-GGUF:Q8_0`
- Inference runtime: llama.cpp
- API: `/v1/systemone`
- llama.cpp version: `0.5.0-dev`, build 11371
- llama.cpp commit: `99b95488cac0f00ce3f05af113a8c1e287753f87`
- OS: Omarchy / Arch Linux
- GPU present: AMD Radeon RX 7800 XT
- Kev execution: CPU-only
- Benchmark threshold: `0.5`

## Frozen phase-1 benchmark

The first Kev comparison uses the frozen **ZOMAH Laya Primitive Diagnostic v0.8**.

- Cases: 36
- Positive cases: 18
- Negative cases: 18
- Benchmark SHA-256: `0e974e7e68a069e1615ba82e26d4551868fc16e5ed17b35872c852b9f097b8d4`
- Predicates: runtime-state change, package-state change, path identity, data removal, replacement, authentication-material change, explicit backup, previous-value knowledge, and explicit inverse availability.

This suite was not designed specifically for Kev. It is used here because its cases, instructions, threshold, and expected labels were already frozen before Kev was tested, giving us a useful controlled comparison without redesigning the benchmark around the new model.

## Phase-1 results

| Model | Backend | Accuracy | Positive | Negative | Strong wrong | Mean HTTP latency |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Julia-1 Q8 | CPU | 23/36 (63.9%) | 8/18 (44.4%) | 15/18 (83.3%) | 10 | 16.42 ms |
| Laya Q8 | CPU | 27/36 (75.0%) | 17/18 (94.4%) | 10/18 (55.6%) | 5 | 51.09 ms |
| Laya Q8 | Vulkan / GPU | 27/36 (75.0%) | 17/18 (94.4%) | 10/18 (55.6%) | 5 | 13.51 ms |
| **Kev-0.8B Q8** | **CPU** | **35/36 (97.2%)** | **17/18 (94.4%)** | **18/18 (100.0%)** | **0** | **~111-124 ms** |

Kev's only miss was `path-002`, where `changes_path_identity` was expected `true` and the model returned approximately `0.4884`, just below the frozen `0.5` threshold. The miss is retained as a failure rather than changing the threshold after seeing the result.

## Repeatability

Three additional CPU runs reproduced:

- 35/36 correct
- 17/18 positive
- 18/18 negative
- 0 strong-wrong cases
- the same `path-002` miss at approximately `0.4884`
- nearly identical probability outputs

Mean HTTP latencies for those repeats were 110.97 ms, 110.75 ms, and 112.46 ms.

## Lean CPU runtime profile

General-purpose llama.cpp defaults allocated much more memory than this decision workload needed. The current lean profile is:

```bash
./build/bin/llama-server \
  -hf ggml-org/Kev-0.8B-GGUF:Q8_0 \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 0 \
  -np 1 \
  -c 512 \
  -b 128 \
  -ub 128 \
  -t 8 \
  -tb 8 \
  --cache-ram 0 \
  --no-cache-prompt \
  -ctxcp 0 \
  --poll 0 \
  --poll-batch 0
```

With that profile:

- benchmark behavior remained 35/36, 97.2%
- mean HTTP latency remained about 111-113 ms
- resident memory after benchmark was about 1.04 GB
- five one-second idle `pidstat` samples reported 0.00% CPU
- the RX 7800 XT remained unused by the decision server

The runtime profile is preserved in [`scripts/start_kev_cpu_lean.sh`](scripts/start_kev_cpu_lean.sh).

## Architecture interpretation

The decision model is **not** policy authority.

The intended ZOMAH pattern remains:

1. Deterministic code constructs the legal decision surface and handles exact machine facts.
2. A small decision model supplies semantic judgment only where deterministic logic cannot resolve the question.
3. Code owns thresholds, escalation policy, validation, and execution.
4. Completion judgment remains separate from deterministic completion verification.

The current Kev result makes a CPU-resident local decision layer operationally plausible. It does not establish production reliability.

## What this benchmark does not claim

- It does not prove Kev is the best decision model overall.
- It does not establish production reliability.
- It does not establish 97.2% expected accuracy outside this frozen 36-case diagnostic.
- It does not justify changing the decision threshold after seeing the result.
- It does not show that larger or differently trained models would not perform better.
- It does not replace deterministic policy, machine-state checks, or completion verification.

## Next phase

The next benchmark will be designed around actual ZOMAH judgment jobs rather than the older Laya diagnostic:

- worker routing
- action gating and escalation
- retrieval relevance
- usable-evidence judgment
- contradiction detection
- suspicious or prompt-injection-like content
- progress / stuckness
- completion judgment
- dynamic action-menu selection
- uncertainty-driven escalation

## Repository structure

```text
kev-decision-benchmark/
├── README.md
├── LICENSE
├── LICENSE-CODE
├── LICENSE-CONTENT
├── LICENSES.md
├── benchmarks/
├── docs/
├── hashes/
├── methodology/
├── report/
├── results/
└── scripts/
```

Raw benchmark cases, runner outputs, and local result files are copied from the canonical lab only after a public-data/privacy audit. Canonical local experiment artifacts are not rewritten in place for publication.

## Licensing

This repository uses split licensing by artifact type. See [`LICENSES.md`](LICENSES.md).

- Code, scripts, and experiment runners: **Apache-2.0**. The root [`LICENSE`](LICENSE) contains the full Apache 2.0 terms, and [`LICENSE-CODE`](LICENSE-CODE) states the code scope.
- Benchmark data, documentation, reports, tables, and figures authored for this project: **CC BY 4.0**. See [`LICENSE-CONTENT`](LICENSE-CONTENT).
- Third-party code, model weights, libraries, and referenced external assets remain under their original licenses.

## Current status

**Phase 1: runtime viability and frozen diagnostic completed.**

Kev-0.8B Q8 is currently the leading small CPU-first candidate tested for ZOMAH. Broader Decision Benchmark v1 validation is pending before any integration decision.
