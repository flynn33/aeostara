# Branch Native Realization Clarification

This document locks the corrected branch model baseline for the Aeostara repository. It supersedes any earlier language that implied platform branches must preserve `main`'s implementation-agnostic posture.

> **Note**: These platform branches are planned to become separate repositories. See [Future Repo Split Plan](future_repo_split_plan.md) for the migration plan.

## Corrected Rule Set

### `main`
- **Code-agnostic** and **behavior-authoritative**
- Source of truth for: contracts, algorithms, interfaces, acceptance targets, architecture intent
- Defines *what* the platform must do, not *how*
- Must not contain compilable source code, platform-specific build systems, or runtime code

### `platform/windows`
- **Windows-native realization branch**
- Implements shared spec behavior using the platform's native toolchain
- May adopt platform-specific patterns and integration points

### `platform/macos`
- **macOS-native realization branch**
- Implements shared spec behavior using the platform's native toolchain
- May adopt platform-specific patterns and integration points
- Build/test proof deferred until work moves to a Mac

### `platform/ios`
- **iOS-native realization branch**
- Implements shared spec behavior using the platform's native toolchain
- May adopt platform-specific patterns and integration points
- Build/test proof deferred until work moves to a Mac

## Key Distinction

**Shared behavior** stays abstract in `main`. **Implementation** is native inside each platform branch. Platform branches are not copies of `main`'s abstraction model — they are native realizations of it.

A platform branch's internal architecture may adopt platform-specific patterns, frameworks, and integration points that would be inappropriate in `main`. This is by design.

## Platform Integration Rules

All platform branches must observe these integration rules:

1. **No direct module-to-module communication** — modules communicate through well-defined interfaces
2. **No module-owned UI** — UI is owned by the application layer, not by core modules
3. **Interface-mediated I/O only** — all I/O goes through interface-provided abstractions

These rules constrain *how* a platform branch integrates its native toolchain, ensuring clean module boundaries.

## Domain Contract Independence

Domain-level contracts (the 11 data types defined in `specs/contracts/`) remain implementation-independent. They define behavior, not hosting. A platform branch's domain module should maintain clean separation between behavioral contracts and platform-specific integration.

## What This Document Prevents

This clarification prevents the drift pattern where `main`'s code-agnostic posture is incorrectly applied to platform branches, blocking valid native integration. Platform branches are explicitly permitted to be fully native.
