# Platform Status Matrix

Last updated: 2026-04-02

> This matrix describes the current state of platform implementation branches. This repository is the **authority/specification repo** — platform verification and release readiness will become the responsibility of future platform repositories. See [Future Repo Split Plan](specs/architecture/future_repo_split_plan.md).

## Branch Status

| Platform | Branch | Implementation Status | Build Verified |
|----------|--------|-----------------------|----------------|
| Windows | `platform/windows` | Reference implementation | Locally proven |
| macOS | `platform/macos` | Source present | Build unverified |
| iOS | `platform/ios` | Source present | Build unverified |

## Build & Test Summary

| Platform | Build Status | Test Status | Notes |
|----------|-------------|-------------|-------|
| Windows | Proven locally (MSVC 2022) | Proven locally (5/5 acceptance scenarios) | No CI workflow yet |
| macOS | Unverified | Unverified | Source written on Windows; CI workflow exists but untriggered |
| iOS | Unverified | Unverified | Source written on Windows; CI workflow exists but untriggered |

**"Proven locally"** means build and test commands have been executed successfully on a local development machine. **"Unverified"** means source code is structurally present but has not been compiled or tested on the target platform.

## Product Behavior Coverage

All three platforms are structurally designed to implement the same behavioral coverage (validate, diff, heal, backup, verification, rollback, audit trail, policy gating). However:

- **Windows**: Behavioral coverage confirmed through local testing
- **macOS / iOS**: Behavioral coverage is structurally present in source but **unverified** through actual execution

## Compliance

Compliance with the root specification policy is:

- **Windows**: Asserted based on local build and test evidence
- **macOS / iOS**: Asserted structurally (source review) but **not verified** through build/test execution

Full compliance verification for macOS and iOS is deferred to the future platform repositories where actual build proof can be obtained.

## CI Workflow Status

| Platform | Workflow File | Status |
|----------|--------------|--------|
| Windows | (not yet created) | Pending |
| macOS | `macos-build-test.yml` | Exists, untriggered on runner |
| iOS | `ios-build-test.yml` | Exists, untriggered on runner |

## Known Gaps

1. **No Windows CI workflow** — builds and tests are proven locally but no automated CI exists
2. **macOS/iOS build-unverified** — source was written on a Windows machine and has not been compiled on actual Apple hardware
3. **CI runner proof missing for all platforms** — no workflow has been successfully triggered on GitHub Actions runners

These gaps will be addressed when platform branches become independent platform repositories with dedicated CI infrastructure.
