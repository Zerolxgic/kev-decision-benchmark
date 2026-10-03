# Runners

This directory will contain audited public copies of benchmark runners used to generate published results.

The phase-1 SystemOne runner sends one frozen predicate question per case to a local llama.cpp `/v1/systemone` endpoint, preserves raw `noul` probabilities, applies the frozen `0.5` threshold, records diagnostic labels, and writes timestamped JSON results.

The exact canonical local runner will be copied here only after privacy/content audit. Public documentation does not substitute for the raw runner artifact.
