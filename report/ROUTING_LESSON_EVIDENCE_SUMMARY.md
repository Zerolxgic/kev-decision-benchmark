# A routing lesson from a small local model

Public-safe evidence summary for review · 5 October 2026

## The lesson

A routing experiment exposed a useful mistake: an uncertain worker choice was automatically being sent to a human. The evidence pointed to a narrower problem in the fallback rule. The next policy kept uncertainty as a request for more model reasoning, while preserving human review as a separate routing outcome.

This is a small development result about separating semantic judgment from routing policy. It does not establish production reliability or remove the need for human authority.

## What was being tested

The worker-routing task chose among four permitted destinations: local inspection, coding, external research, and human review. A decomposed representation scored four signals: local state, code work, external research, and human authority. Deterministic code owned which destinations were legal and how scores became routes.

The surrounding development reports identify Kev-0.8B Q8 running CPU-only through llama.cpp's SystemOne interface. The holdout and retrospective reports do not independently pin a model-file hash, exact runtime revision, or complete runtime settings. Those details still need to be tied to the routing runs before claiming exact reproducibility. The runtime revision published for the earlier primitive benchmark should not be silently carried over.

For the strict routing rule, exactly one legal feature at or above 0.5 produced a semantic resolution. Zero or multiple qualifying features left the decision unresolved. This was a decision threshold, not demonstrated confidence calibration.

## What the fresh holdout showed

The v0.1 report describes 16 fresh cases, balanced across the four destinations, with the feature contract, policy, runner, evaluator, and cases hashed before the run.

- Strict semantic coverage: 12 resolved cases out of 16, or 75%.
- Accuracy within those resolved cases: 12 correct out of 12.
- Final routing under policy v0.1: 15 correct out of 16, or 93.8%.
- Unresolved cases: four human-review fallbacks and no stronger-model escalations.
- A separate forced-winner score was also 15/16. This is a different measure from final policy routing, even though the totals match.

The wrong final route should have gone to research. Its external-research score was 0.6887, local-state score 0.5759, human-authority score 0.2092, and code-work score 0.0804. Research ranked highest, but both research and local state crossed the threshold. The strict rule therefore left the case unresolved.

Policy v0.1 sent unresolved work to human review whenever that destination was legal. That fallback created the wrong route in this case. A legal human-review option did not by itself establish that the task needed human authority.

## What changed in policy v0.2

Policy v0.2 removed the automatic unresolved-to-human-review fallback. Exactly one qualifying legal feature still resolved directly; every other unresolved state escalated to a stronger model. Human review remained an available semantic destination, and hard permissions remained the responsibility of deterministic code.

The revised policy was evaluated retrospectively on 40 already observed cases:

- Original development set: 6/8 resolved, all six correct, two escalations.
- Boundary set: 8/8 resolved, all eight correct.
- Minimal-pair set: 8/8 resolved, all eight correct.
- Reused v0.1 holdout: 12/16 resolved, all 12 correct, four escalations.

Combined: 34/40 resolved, giving 85% coverage; 34/34 resolved routes were correct; six cases escalated. The report records zero wrong operational routes under this policy.

The six escalations must stay visible in that result. They were not six demonstrated successful stronger-model answers. The report does not establish their downstream outcomes. The former wrong human-review route became an escalation, rather than a proven correct research route.

## Evidence limits and the next test

All 40 cases had already influenced development. They cannot establish fresh-holdout performance for v0.2, and 34/34 should never be presented as 100% accuracy across all tasks. These results also do not measure end-to-end task completion, escalation cost, production failure rates, or generalization to other models and workloads.

A defensible next evaluation would freeze the revised policy, feature contract, runner, evaluator, promotion criteria, and a genuinely new holdout before testing. It should report resolved accuracy and coverage separately, evaluate escalation outcomes, and preserve human-authority and permission checks. Live shadow evaluation would still be needed before an integration decision.

## Source status

The routing numbers above were checked against the private “Worker Routing Holdout v0.1 Findings” and “Worker Routing Policy v0.2 Retrospective” reports. This summary explains their method and arithmetic; it is not an independent rerun or a publicly reproducible routing evidence package. No public routing case set or raw-output package was verified for this summary.

The [public Kev Decision Benchmark](https://github.com/Zerolxgic/kev-decision-benchmark/blob/main/README.md) documents the separate, earlier frozen 36-case primitive diagnostic and the advisory-model architecture. It is background, not evidence for these 40 routing cases.

## Possible post angle

One wrong route taught me to separate two questions: which worker fits the task, and what should happen when that choice is uncertain? The revised fallback preserved uncertainty as escalation. On 40 reused development cases, it resolved 34 correctly and escalated six. The next test needs fresh cases.
