# Native Target Architecture

## Model

Aeostara is structured as:
- **Shared specifications** on `main` — language-agnostic contract schemas, pseudo code algorithms, interface definitions
- **Platform implementations** on `platform/*` branches — native code implementing the specs

## Shared Spec Responsibilities

The specifications on `main` define:
- 11 contract data types (JSON Schema)
- 9 algorithms (pseudo code)
- 5 interfaces (pseudo code)
- Acceptance scenarios
- Compliance rules

## Platform Implementation Responsibilities

Each `platform/*` branch independently implements:
- All 11 contracts in the platform's native language
- All algorithms following the pseudo code specifications
- All 5 interfaces with platform-appropriate implementations
- Platform-specific shell (CLI, GUI, or mobile app)
- Platform-specific build and test infrastructure

## Implementation Languages

| Platform | Language | Build System | Test Framework |
|----------|----------|-------------|----------------|
| Windows | C++20 | CMake + MSVC | CppUnitTest |
| macOS | Swift | SwiftPM or Xcode | XCTest |
| iOS | Swift / SwiftUI | SwiftPM or Xcode | XCTest / XCUITest |

## Shared Specs vs Native Realization

Shared behavior lives in `main` specs — code-agnostic, defining *what* the platform must do, not *how*. Native implementation lives in platform branches — each branch realizes the spec using its platform's native toolchain and patterns. Platform branches may integrate with their platform's Forsetti framework while observing Forsetti boundary rules. Branch internals are not required to preserve `main`'s implementation-agnostic posture.

## Shared Test Fixtures

JSON test fixtures in `fixtures/` are shared across all platforms via merge from `main`. All platforms test against the same input data to ensure deterministic cross-platform behavior.
