# Platform Status Matrix

Last updated: 2026-03-21

## Branch Status

| Platform | Branch | Status | Version |
|----------|--------|--------|---------|
| Windows | `platform/windows` | Reference implementation | v0.1.0 |
| macOS | `platform/macos` | Source-complete, build-unverified | v0.1.0 |
| iOS | `platform/ios` | Source-complete, build-unverified | v0.1.0 |

## Build Status

| Platform | Builds | Toolchain | Build Command | Dependencies |
|----------|--------|-----------|---------------|-------------|
| Windows | YES (proven locally) | MSVC 2022, CMake 3.28+, vcpkg | `cmake --preset debug && cmake --build --preset debug` | nlohmann/json |
| macOS | Unverified | Swift 5.9+, SwiftPM | `swift build` | Foundation only |
| iOS | Unverified | Swift 5.9+, SwiftPM, Xcode 15+ | `swift build` / `xcodebuild -scheme AeostaraApp -destination 'platform=iOS Simulator'` | Foundation only |

## Test Status

| Platform | Tests Run | Framework | Test Command | Acceptance Scenarios |
|----------|-----------|-----------|-------------|---------------------|
| Windows | YES (proven locally) | CppUnitTest | `ctest --preset debug` | 5 (valid, schema fail, policy block, repair, rollback) |
| macOS | Unverified | XCTest | `swift test` | 5 (matching Windows) |
| iOS | Unverified | XCTest + XCUITest | `swift test` / `xcodebuild test -scheme AeostaraTests -destination 'platform=iOS Simulator'` | 5 + UI flow tests |

## Product Behavior Coverage

| Behavior | Windows | macOS | iOS |
|----------|---------|-------|-----|
| validate command | YES | YES | YES |
| diff command | YES | YES | YES |
| heal command | YES | YES | YES |
| Backup created | YES | YES | YES |
| Verification after repair | YES | YES | YES |
| Rollback on failure | YES | YES | YES |
| Audit trail output | YES | YES | YES |
| Policy gating | YES | YES | YES |

## Compliance Status

| Rule | Windows | macOS | iOS |
|------|---------|-------|-----|
| R001: Native technologies only | PASS | PASS | PASS |
| R005: All classes final, constructor DI | PASS | PASS | PASS |
| R006: One-way dependencies | PASS | PASS | PASS |
| R007: No Forsetti in core | PASS | PASS | PASS |
| R008: Deterministic behavior | PASS | PASS | PASS |
| R009: Proprietary license | PASS | PASS | PASS |
| No Python in product | PASS | PASS | PASS |
| No YAML in product | PASS | PASS | PASS |
| Host-agnostic core | PASS | PASS | PASS |

## CI Workflow Status

| Platform | Workflow File | CI Proven on Runner |
|----------|--------------|-------------------|
| Windows | (not yet created) | NO |
| macOS | `macos-build-test.yml` | NO (awaiting first push trigger) |
| iOS | `ios-build-test.yml` | NO (awaiting first push trigger) |

## Blockers

| Platform | Blocker | Severity | Notes |
|----------|---------|----------|-------|
| Windows | No platform-specific CI workflow | LOW | Builds and tests proven locally |
| macOS | CI unproven on actual GitHub Actions macOS runner | LOW | Workflow exists, awaiting trigger |
| iOS | CI unproven on actual GitHub Actions iOS simulator | LOW | Workflow exists, awaiting trigger |

## Notes

- "Proven locally" = build and test commands have been executed successfully on a local machine
- "Documented" = build and test commands are specified in platform README and manifest, implementation complete, but not yet verified on a CI runner
- Windows uses C++20 (AeostaraCore) with a platform-specific CLI shell
- macOS and iOS use native Swift implementations (no shared C++ core, no Obj-C++ bridge)
- Apple branches are source-complete but build-unverified (remediation performed on Windows)
