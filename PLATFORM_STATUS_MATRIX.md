# Platform Status Matrix

Last updated: 2026-03-21

## Branch Status

| Platform | Branch | Status | Version |
|----------|--------|--------|---------|
| Windows | `platform/windows` | Reference implementation | v0.1.0 |
| macOS | `platform/macos` | Implemented | v0.1.0 |
| iOS | `platform/ios` | Alpha (source-complete) | v0.1.0 |

## Build Status

| Platform | Builds | Toolchain | Build Command | Dependencies |
|----------|--------|-----------|---------------|-------------|
| Windows | YES (proven locally) | MSVC 2022, CMake 3.28+, vcpkg | `cmake --preset debug && cmake --build --preset debug` | nlohmann/json |
| macOS | YES (documented) | Apple Clang, CMake 3.28+, Ninja | `cmake -B build -G Ninja && cmake --build build` | nlohmann/json, Catch2 |
| iOS | YES (documented) | Xcode, Swift 5.9+, Apple Clang C++20 | `xcodebuild build -project Aeostara.xcodeproj -scheme AeostaraApp -sdk iphonesimulator` | nlohmann/json (embedded) |

## Test Status

| Platform | Tests Run | Framework | Test Command | Acceptance Scenarios |
|----------|-----------|-----------|-------------|---------------------|
| Windows | YES (proven locally) | CppUnitTest | `ctest --preset debug` | 5 (valid, schema fail, policy block, repair, rollback) |
| macOS | YES (documented) | Catch2 | `ctest --test-dir build` | 5 (matching Windows) |
| iOS | YES (documented) | XCTest + UI tests | `xcodebuild test -project Aeostara.xcodeproj -scheme AeostaraTests -sdk iphonesimulator` | Bridge tests + UI smoke |

## Product Behavior Coverage

| Behavior | Windows | macOS | iOS |
|----------|---------|-------|-----|
| validate command | YES | YES | YES (via bridge) |
| diff command | YES | YES | YES (via bridge) |
| heal command | YES | YES | YES (via bridge) |
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
- All three platforms share the same C++20 core (AeostaraCore) with platform-specific shells
- iOS uses an Obj-C++ bridge (AeostaraKit) between the SwiftUI app layer and the C++ core
