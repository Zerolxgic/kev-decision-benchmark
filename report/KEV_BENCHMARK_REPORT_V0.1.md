# Kev Decision Benchmark v0.1

## Summary

This report documents the first controlled evaluation of `ggml-org/Kev-0.8B-GGUF:Q8_0` as a CPU-first local decision model for the ZOMAH agent architecture through llama.cpp's `/v1/systemone` interface.

The initial question was operational as much as semantic: can a small decision model remain resident on CPU, produce useful typed judgments at low enough latency for orchestration, and avoid consuming the RX 7800 XT that is reserved for larger local models such as Gemma?

The phase-1 result is promising. On a frozen 36-case diagnostic originally created for Laya, Kev scored 35/36 (97.2%), with 17/18 positive cases correct, all 18 negative cases correct, zero strong-wrong cases, and one borderline miss at 0.4884 against a fixed 0.5 threshold. The result repeated across multiple runs with nearly identical probabilities.

A lean llama.cpp server profile reduced resident memory from roughly 4.9 GB under general-purpose defaults to roughly 1.0 GB while preserving the same benchmark result and roughly 111-113 ms mean local HTTP latency. Interval-based idle sampling showed 0.00% CPU across five one-second samples. The decision server remained CPU-only.

## Research question

Can Kev-0.8B act as a small always-resident semantic judgment layer inside ZOMAH while deterministic code continues to own exact machine facts, policy, validation, execution, and completion verification?

## Evidence used

The first Kev evaluation intentionally reuses the frozen ZOMAH Laya Primitive Diagnostic v0.8 rather than creating a Kev-specific test after seeing Kev's behavior.

- Cases: 36
- Positives: 18
- Negatives: 18
- Threshold: 0.5
- Benchmark SHA-256: `0e974e7e68a069e1615ba82e26d4551868fc16e5ed17b35872c852b9f097b8d4`

The suite covers nine narrow semantic predicates: runtime-state change, package-state change, path identity, data removal, replacement, authentication-material change, explicit backup existence, previous-value knowledge, and explicit inverse availability.

This is controlled comparative evidence, not a production-reliability benchmark.

## Runtime

- OS: Omarchy / Arch Linux
- llama.cpp: 0.5.0-dev, build 11371
- llama.cpp commit: `99b95488cac0f00ce3f05af113a8c1e287753f87`
- API: `/v1/systemone`
- Model: `ggml-org/Kev-0.8B-GGUF:Q8_0`
- Execution: CPU-only
- GPU present but unused by Kev: AMD Radeon RX 7800 XT

## Comparative results

| Model | Backend | Accuracy | Positive | Negative | Strong wrong | Mean HTTP latency |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Julia-1 Q8 | CPU | 23/36 (63.9%) | 8/18 | 15/18 | 10 | 16.42 ms |
| Laya Q8 | CPU | 27/36 (75.0%) | 17/18 | 10/18 | 5 | 51.09 ms |
| Laya Q8 | Vulkan / GPU | 27/36 (75.0%) | 17/18 | 10/18 | 5 | 13.51 ms |
| Kev-0.8B Q8 | CPU | 35/36 (97.2%) | 17/18 | 18/18 | 0 | 123.82 ms initial |

Kev's only failure was `path-002`, where the expected answer was `true` and the model returned approximately 0.4884. The threshold was not changed after observing the result.

## Repeatability

Three additional runs preserved the same 35/36 result, the same single miss, zero strong-wrong cases, and nearly identical probabilities. Mean HTTP latencies were 110.97 ms, 110.75 ms, and 112.46 ms.

This establishes execution stability under the tested setup. It does not create new distributional evidence because the same frozen cases were replayed.

## Runtime tuning

The initial server profile used llama.cpp defaults intended for general-purpose model serving. After repeated tests, resident memory reached roughly 4.9 GB, far above the approximately 812 MB Q8 model artifact itself.

A deliberately lean profile constrained the server to the workload actually required:

- CPU-only: `-ngl 0`
- one parallel slot: `-np 1`
- context: `-c 512`
- batch: `-b 128`
- microbatch: `-ub 128`
- threads: `-t 8`
- batch threads: `-tb 8`
- cache RAM disabled
- prompt cache disabled
- context checkpoints disabled
- CPU polling disabled

Under the lean profile, resident memory after benchmarking was approximately 1.04 GB, mean HTTP latency remained around 111-113 ms, and semantic behavior remained 35/36. Five one-second `pidstat` samples showed 0.00% idle CPU.

## Architectural interpretation

The useful result is not that Kev should control ZOMAH. The useful result is that a small CPU-resident decision layer now looks operationally plausible.

The intended architecture remains:

1. deterministic code constructs the legal action surface and handles exact facts;
2. a decision model supplies fuzzy semantic judgment inside that surface;
3. code owns thresholds, escalation, validation, and execution;
4. apparent completion remains separate from deterministic proof of completion.

Kev's current profile fits that role better than the smaller Julia-1 and Laya candidates tested in this narrow phase, but the evidence is not yet broad enough for permanent selection.

## Limitations

- The benchmark contains only 36 cases.
- It was designed originally to diagnose Laya, not Kev.
- Repeat runs test stability, not generalization.
- The score should not be read as expected production accuracy.
- No conclusion is made yet about larger Kev variants, Clef, OpenJev, or other decision models.
- The current context size of 512 is a deliberately lean experimental profile and may need expansion for broader ZOMAH tasks.

## Next phase

Decision Benchmark v1 should be created and frozen around actual ZOMAH judgment jobs before testing Kev against it. Planned families include worker routing, action gating, retrieval relevance, usable-evidence judgment, contradiction detection, suspicious-content detection, progress/stuckness, completion judgment, dynamic action-menu selection, and uncertainty-driven escalation.

Only after that broader test should Kev move from 'leading candidate' toward an integration decision.
