# Roadmap Separation

This roadmap separates semantic authority work from platform implementation work.

## Track A: Downstream ASH Conformance (current)

Scope:

- Reset architecture authority language
- Replace drift-first contracts/algorithms with ASH-aligned artifacts
- Rebuild acceptance and traceability around ASH conformance
- Update CI gates to prevent regression to removed drift/diff authority

Exit criteria:

- ASH is explicit upstream semantic authority
- Superseded drift-first artifacts are absent
- Conformance artifacts and CI checks are in place

## Track B: Platform Realization and Release Verification

Scope:

- Platform-specific build/test/release validation in platform repos
- Native runtime integration and production hardening

Dependency:

Track B must consume the conformance surface produced by Track A.

## Track C: Future Upstream Evolution (out of scope here)

Any semantic evolution of ASH belongs upstream and is not performed in this repository during Aeostara remediation.
