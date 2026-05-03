
# Branch Alignment Contract - Superseded for Base Completion

This document is retained as a historical note and downstream handoff concept. Branch alignment is not an active Aeostara base-design completion gate.

## Superseding Rule

Aeostara completion is validated by base-design contracts, ASH traceability, fixture outputs, diagnostic chains, recovery consistency, JSON semantics, and downstream handoff sufficiency. It is not validated by requiring platform branches or native implementation source files.

## Current Use

Downstream repos may adapt the platform-repo templates under `templates/platform_repo/` to report their own branch/module mapping. Those reports belong to platform repositories and do not make Aeostara depend on them.
