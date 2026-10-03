# Phase 1 summary

## Frozen benchmark

- Benchmark: ZOMAH Laya Primitive Diagnostic v0.8
- Cases: 36
- Threshold: 0.5
- SHA-256: `0e974e7e68a069e1615ba82e26d4551868fc16e5ed17b35872c852b9f097b8d4`

## Comparison

| Model | Backend | Accuracy | Positive | Negative | Strong wrong | Mean HTTP latency |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Julia-1 Q8 | CPU | 23/36 (63.9%) | 8/18 (44.4%) | 15/18 (83.3%) | 10 | 16.42 ms |
| Laya Q8 | CPU | 27/36 (75.0%) | 17/18 (94.4%) | 10/18 (55.6%) | 5 | 51.09 ms |
| Laya Q8 | Vulkan / GPU | 27/36 (75.0%) | 17/18 (94.4%) | 10/18 (55.6%) | 5 | 13.51 ms |
| Kev-0.8B Q8 | CPU | 35/36 (97.2%) | 17/18 (94.4%) | 18/18 (100.0%) | 0 | 123.82 ms initial |

## Kev repeatability

Three additional CPU runs produced the same semantic result:

| Run | Accuracy | Strong wrong | Borderline | Mean HTTP latency |
| --- | ---: | ---: | ---: | ---: |
| Repeat 1 | 35/36 (97.2%) | 0 | 2 | 110.97 ms |
| Repeat 2 | 35/36 (97.2%) | 0 | 2 | 110.75 ms |
| Repeat 3 | 35/36 (97.2%) | 0 | 2 | 112.46 ms |

The same single miss persisted: `path-002`, expected `true`, score approximately `0.4884`.

## Lean runtime profile

After reducing general-purpose llama.cpp context and batch allocations, Kev retained the same 35/36 semantic result while resident memory dropped from roughly 4.9 GB to roughly 1.0 GB.

Two observed lean runs:

- 35/36, 97.2%, mean HTTP latency 112.97 ms
- 35/36, 97.2%, mean HTTP latency 111.49 ms

Post-benchmark resident memory was approximately 1.04 GB. Five one-second `pidstat` idle samples reported 0.00% CPU. The decision server remained CPU-only, leaving the RX 7800 XT unused.

## Current interpretation

Kev-0.8B Q8 is the strongest small CPU-first candidate tested in phase 1. This result justifies broader ZOMAH-specific evaluation but does not establish production reliability or permanent model selection.
