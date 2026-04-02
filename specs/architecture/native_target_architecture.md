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

## Platform Toolchain Independence

Each platform implementation chooses its own native language, build system, and test framework. The root authority repository does not prescribe these choices. Current platform branches have made their own toolchain selections, documented within those branches. Future platform repositories will own their toolchain decisions independently.

## Shared Specs vs Native Realization

Shared behavior lives in `main` specs — code-agnostic, defining *what* the platform must do, not *how*. Native implementation lives in platform branches — each branch realizes the spec using its platform's native toolchain and patterns. Branch internals are not required to preserve `main`'s implementation-agnostic posture.

## Shared Test Fixtures

JSON test fixtures in `fixtures/` are shared across all platforms via merge from `main`. All platforms test against the same input data to ensure deterministic cross-platform behavior.
