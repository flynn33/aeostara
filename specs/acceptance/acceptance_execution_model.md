# Acceptance Execution Model

This document defines how conformance acceptance is evaluated in this specification repository.

## Repository-Level Validation

Repository automation validates:

1. Required conformance docs exist.
2. Required ASH-aligned contracts exist and validate.
3. Required algorithm specs exist.
4. Legacy drift-first contracts are marked non-authoritative.
5. Traceability and remediation acceptance artifacts exist.

## Implementation-Level Validation

Platform implementation repos validate runtime behavior against these acceptance scenarios through platform-native test harnesses.

## Separation Rule

This repository proves specification coherence and conformance surface integrity.
Platform repos prove executable behavior.

Both layers are required for end-to-end conformance.
