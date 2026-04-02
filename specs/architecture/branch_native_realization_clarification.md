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
- Implements shared spec behavior using C++20, MSVC, CMake, vcpkg
- May align to the Windows Forsetti framework and Windows-native implementation model
- Must observe Forsetti boundary rules (see below)

### `platform/macos`
- **macOS-native realization branch**
- Implements shared spec behavior using Swift, SwiftPM, XCTest
- May align to the macOS Forsetti framework expectations
- Must observe Forsetti boundary rules (see below)
- Build/test proof deferred until work moves to a Mac

### `platform/ios`
- **iOS-native realization branch**
- Implements shared spec behavior using Swift, SwiftUI, SwiftPM, XCTest/XCUITest
- May align to the iOS Forsetti framework expectations
- Must observe Forsetti boundary rules (see below)
- Build/test proof deferred until work moves to a Mac

## Key Distinction

**Shared behavior** stays abstract in `main`. **Implementation** is native inside each platform branch. Platform branches are not copies of `main`'s abstraction model — they are native realizations of it.

A platform branch's internal architecture may adopt platform-specific patterns, frameworks, and integration points that would be inappropriate in `main`. This is by design.

## Binding Forsetti Boundary Rules

All platform branches must observe these Forsetti boundary rules:

1. **No framework modification** — platform branches must not modify the Forsetti framework itself
2. **No direct module-to-module communication** — modules communicate through framework-mediated channels
3. **No direct OS communication** — OS access is framework-mediated
4. **No module-owned UI** — UI is owned by the framework, not by the module
5. **Framework-mediated I/O only** — all I/O goes through framework-provided interfaces

These rules constrain *how* a platform branch integrates with Forsetti, not *whether* it may integrate at all. Platform-native Forsetti integration is valid and expected.

## Domain Contract Independence

Domain-level contracts (the 11 data types defined in `specs/contracts/`) remain Forsetti-independent. They define behavior, not hosting. A platform branch's domain module should not import Forsetti framework headers — Forsetti integration happens at the platform services or application layer.

## What This Document Prevents

This clarification prevents the drift pattern where `main`'s code-agnostic posture is incorrectly applied to platform branches, blocking valid native integration. Platform branches are explicitly permitted to be fully native.
