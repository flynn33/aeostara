
# Branching Strategy - Base Repository

Aeostara's base repository uses normal source-control branches for specification work. Platform implementation branches are not required for Aeostara base-design completion.

## Base Branch Expectations

The base repository must keep these artifacts valid on its main integration branch:

- ASH baseline reference and bindings.
- Contract schemas and examples.
- Conformance fixtures with expected outputs.
- CI validators.
- Downstream handoff templates.

## Platform Implementation Repositories

Windows, Mac, and iOS repositories manage their own implementation branches. They consume Aeostara by version pin and prove conformance with the downstream handoff templates.
