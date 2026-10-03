# Collaboration model

This benchmark is a human-directed, AI-collaborative research project.

## Roles

### Zerrius

- Sets the research direction and decides which questions are worth testing.
- Runs the experiments locally and controls the execution environment.
- Reviews outputs and decides when results are convincing, suspicious, or worth challenging with stronger tests.
- Makes the final architecture decisions for ZOMAH.
- Controls what material is published.

### ChatGPT

- Collaborates on experiment design and benchmark progression.
- Helps identify confounds, alternative explanations, and stronger follow-up tests.
- Analyzes result patterns and separates observed result, interpretation, and architecture decision.
- Assists with documentation, benchmark packaging, public synthesis, and release preparation.

### Other AI tools

Additional coding agents and language models may be used as implementation tools where appropriate. Their use does not replace the provenance of the actual benchmark artifacts, runners, inputs, outputs, hashes, and local measurements.

## Responsibility and evidence

AI assistance is disclosed because it materially contributes to the research process. It is not presented as independent experimental evidence.

The benchmark's claims are grounded in recorded experiment artifacts and observed results. Zerrius remains responsible for executing experiments, controlling what enters the system, deciding whether additional tests are required, and adopting or rejecting architecture conclusions.

## Working pattern

The recurring loop is:

1. Form a hypothesis or identify a failure.
2. Design a bounded test.
3. Freeze cases, instructions, thresholds, and hashes where appropriate.
4. Run the test locally.
5. Inspect the evidence together.
6. Challenge the current interpretation with a stronger evidence class when warranted.
7. Update architecture only when the evidence justifies it.

This process intentionally distinguishes proposal, experiment, observation, interpretation, architecture decision, implementation, verification, and acceptance.
