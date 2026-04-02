# Acceptance Execution Model

This document describes how the 5 shared acceptance scenarios defined in [acceptance_targets.md](acceptance_targets.md) are verified, and the division of responsibility between the root authority repo and platform implementation repos.

## Authority Specification

The authority spec defines 5 shared behavior scenarios that all platform implementations must pass:

| # | Scenario | Behavior |
|---|----------|----------|
| 1 | Valid Config — No Drift | validate returns valid=true, exit 0 |
| 2 | Invalid Config — Parse Error | validate returns valid=false, exit 2 |
| 3 | Policy Block — Critical Invariant Violation | heal returns blocked, exit 1 |
| 4 | Successful Repair | backup + heal + audit trail, exit 0 |
| 5 | Forced Rollback — Verification Failure | rollback executed + audit records |

All 5 scenarios are **required** for every platform implementation. The authority spec is not weakened by the execution model below.

## Root CLI Smoke Runner (`ci/acceptance_runner.py`)

The root repo provides a black-box CLI smoke runner that invokes a built platform binary and validates output against expected behavior.

**What it covers:** Scenarios 1–4. These scenarios can be fully exercised by invoking the binary with appropriate fixture files and checking exit codes and JSON output.

**What it does not cover:** Scenario 5 (Forced Rollback — Verification Failure). This scenario requires injecting a fault into the verify/rollback path — specifically, a mock or stub file system that returns corrupted content on the post-repair verification re-read. This fault injection cannot be performed from outside the binary via CLI invocation alone.

## Platform-Native Rollback Verification

Scenario 5 must be proven in each platform's native test infrastructure using an in-process test harness that can:

1. Substitute a mock/stub `IFileSystem` implementation
2. Configure the stub to return bad content on the verification re-read after repair
3. Assert that the healing engine triggers rollback
4. Assert that audit records contain `VerificationFailed` and `RollbackExecuted` events

This requires access to the platform's dependency injection seam (constructor DI on `IFileSystem`) and cannot be truthfully replicated by a generic binary runner.

## Responsibility Summary

| Verification | Owner | Method |
|-------------|-------|--------|
| Scenarios 1–4 (CLI-verifiable) | Root repo smoke runner + platform repos | Black-box binary invocation with shared fixtures |
| Scenario 5 (Forced Rollback) | Platform repos only | Platform-native test harness with mock/stub file system |
| All 5 scenarios (complete proof) | Platform repos | Combination of CLI smoke + native rollback test |

## Why This Separation Exists

The root authority repo defines *what* must happen. It can verify behaviors that are observable from outside the binary (exit codes, JSON output, file side effects). But Scenario 5 requires observing internal behavior (rollback triggered after verification failure) that is only testable when the test harness controls the file system abstraction. Claiming to verify this scenario from a black-box runner would be false proof.
