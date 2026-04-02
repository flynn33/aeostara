# Planned Agnostic Core File Index

> **ALL ENTRIES IN THIS DOCUMENT ARE DEFERRED.** None of these files exist yet. Their content will be created during the Agnostic Core design phase, which follows the current repository realignment phase. Do not create these files until the Agnostic Core design phase begins.

---

## Purpose

This index registers files planned for the future Agnostic Core design phase. It ensures the project has a clear record of what needs to be designed without inventing content prematurely.

---

## Category 1: Core Abstraction Layer

| Planned File | Purpose | Status | Dependency |
|-------------|---------|--------|------------|
| `specs/core/agnostic_type_definitions.md` | Language-neutral representations of the 11 contract types, defining how platforms consume them abstractly | Deferred | Agnostic Core design phase |
| `specs/core/agnostic_algorithm_orchestration.md` | Platform-independent healing flow coordination, defining the abstract execution model | Deferred | Agnostic Core design phase |
| `specs/core/agnostic_interface_bindings.md` | How platform implementations bind to the 5 core interfaces programmatically | Deferred | Agnostic Core design phase |

## Category 2: ASH Kernel Formalization

| Planned File | Purpose | Status | Dependency |
|-------------|---------|--------|------------|
| `specs/ash/encoded_state_model.md` | Formal specification of the encoded state representation | Deferred | Agnostic Core design + ASH deepening track |
| `specs/ash/drift_distance_metric.md` | Specification of drift distance measurement and comparison semantics | Deferred | Agnostic Core design + ASH deepening track |
| `specs/ash/correction_semantics.md` | Formal specification of correction operations and their properties | Deferred | Agnostic Core design + ASH deepening track |
| `specs/ash/confidence_model.md` | Specification of confidence scoring for repair decisions (future) | Deferred | ASH deepening track, later phase |
| `specs/ash/pattern_reasoning.md` | Specification of pattern recognition and reasoning in healing decisions (future) | Deferred | ASH deepening track, later phase |

## Category 3: Platform Consumption Protocol

| Planned File | Purpose | Status | Dependency |
|-------------|---------|--------|------------|
| `specs/core/platform_compliance_protocol.md` | How a platform repo validates its implementation against the core spec | Deferred | Agnostic Core design phase + repo split |
| `specs/core/cross_platform_determinism_verification.md` | Protocol for verifying deterministic behavior across platforms using shared fixtures | Deferred | Agnostic Core design phase |
| `specs/core/fixture_based_acceptance_automation.md` | Automation framework for running acceptance scenarios in platform repos against core fixtures | Deferred | Agnostic Core design phase + repo split |

---

## Notes

- The directory paths above (`specs/core/`, `specs/ash/`) are tentative and may change during the Agnostic Core design phase
- No content should be invented for these files until the design phase produces formal decisions
- This index may be updated as planning progresses, but files should not be created until their dependencies are met
