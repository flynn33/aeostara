
# Base-to-Platform Versioning

Downstream platform repos must explicitly pin the Aeostara base design they implement.

## Aeostara Version Fields

A downstream conformance report must include:

- Aeostara repository URL.
- Aeostara commit SHA or released tag.
- ASH baseline commit recorded by Aeostara.
- Conformance manifest version.
- Schema example set version.
- Fixture manifest version.

## Compatibility Rule

A downstream repo is compatible with an Aeostara version only when it passes that version's schema, fixture, traceability, diagnostic-chain, recovery, JSON semantics, and handoff gates.

## Upgrade Rule

When Aeostara changes a contract or fixture expectation, downstream repos must rerun all affected conformance vectors and update their deviation log before claiming compatibility.
