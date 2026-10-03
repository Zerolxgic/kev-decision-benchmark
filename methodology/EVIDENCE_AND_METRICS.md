# Evidence and metrics

## Evidence classes

This repository keeps different evidence classes separate rather than treating all percentages as interchangeable.

### Frozen diagnostic

A benchmark whose cases, expected labels, predicate instructions, threshold, and hash were fixed before the Kev run. The current phase-1 comparison uses the frozen ZOMAH Laya Primitive Diagnostic v0.8.

### Repeatability run

A repeat of the same frozen benchmark under the same model/runtime configuration. Repeatability checks test execution stability; they do not broaden the task distribution.

### Runtime/resource measurement

Measurements such as mean HTTP round-trip latency, resident memory, idle CPU, and GPU usage. These describe operational cost, not semantic accuracy.

### Future ZOMAH-specific holdout

A new benchmark designed around actual ZOMAH judgment jobs. It should be created and frozen before evaluating Kev against it, with care taken not to tune cases around known Kev behavior.

## Phase-1 metrics

### Accuracy

A `noul` probability is converted to a boolean using the frozen threshold `0.5`.

- score >= 0.5 -> `true`
- score < 0.5 -> `false`

Accuracy is the number of expected booleans matched divided by total cases.

### Positive and negative accuracy

Positive and negative cases are reported separately because small decision models can show strong polarity bias. Aggregate accuracy alone can hide that asymmetry.

### Strong-wrong

Diagnostic only. A case is marked strong-wrong when:

- expected `true` and score <= 0.20, or
- expected `false` and score >= 0.80.

This is not a separate production threshold. It is a way to distinguish confident semantic failure from a near-boundary miss.

### Borderline

Scores between `0.40` and `0.60` are tagged as borderline for diagnostics. The actual pass/fail threshold remains `0.5`.

### Latency

Current latency is measured as local HTTP round-trip time through llama.cpp `/v1/systemone`. It is not directly interchangeable with direct in-process PyTorch inference time unless the measurement paths are matched.

### Memory

Resident memory is recorded from Linux process metrics (`VmRSS` / RSS). Peak resident memory is recorded as `VmHWM` when relevant.

### Idle CPU

Idle CPU is measured using interval-based process sampling such as `pidstat`, not process-lifetime `%CPU` averages.

## Interpretation rules

- Do not change a frozen threshold after seeing a model result to improve the score.
- Do not treat repeat runs as independent distributional evidence.
- Do not infer production reliability from a 36-case diagnostic.
- Preserve wrong cases, including borderline misses.
- Keep deterministic policy and exact machine facts outside the decision model.
- Separate model completion judgment from deterministic completion verification.
- Record runtime configuration alongside semantic results because general-purpose serving defaults can materially affect resource cost.
