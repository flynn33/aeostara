> **ARCHIVED** — This document records the drift correction pass of 2026-03-22. Terminology from that era has since been updated. This document is retained as a historical record of the structural corrections made.

# Repository Branch Drift Matrix

Date: 2026-03-22 (archived 2026-04-02)
Status: Post-alignment correction pass (historical)

## Branch Status

| Branch | Purpose | Old Wording Issue | Corrected Wording | Residual Drift |
|--------|---------|-------------------|-------------------|----------------|
| `main` | Code-agnostic specs | "host-agnostic core" applied too broadly; implied platform branches must preserve implementation agnosticism | Code-agnostic and behavior-authoritative; platform branches are native realization branches | None |
| `platform/windows` | Windows-native realization | R003 blanket-blocked valid native integration; "host-agnostic core" language | Boundary compliance with precise rules; Windows-native integration permitted | None |
| `platform/macos` | macOS-native realization | R003 blanket-blocked valid native integration; "host-agnostic domain" language | Boundary compliance; macOS-native integration permitted at services layer | Build/test proof deferred (Windows PC) |
| `platform/ios` | iOS-native realization | R003 blanket-blocked valid native integration; "host-agnostic domain" language | Boundary compliance; iOS-native integration permitted at services layer | Build/test proof deferred (Windows PC) |

## Files Changed Per Branch

### `main`
| File | Change |
|------|--------|
| `README.md` | Branch model: "native realization branches" added; compliance: "host-agnostic core" replaced with code-agnostic specs |
| `specs/architecture/compliance_rules.md` | Rule 5: "Host-agnostic core" replaced with "Code-agnostic specs"; Rule 6: updated to boundary compliance |
| `specs/architecture/product_boundaries.md` | "stays host-agnostic" replaced with "`main` specs remain code-agnostic; platform branches are native realization branches" |
| `specs/architecture/branching_strategy.md` | Added "native realization branches" section explaining platform branches need not preserve `main`'s abstraction posture |
| `specs/architecture/native_target_architecture.md` | Added "Shared Specs vs Native Realization" section |
| `specs/architecture/branch_native_realization_clarification.md` | **Created** — locks corrected baseline |
| `specs/architecture/repo_branch_drift_matrix.md` | **Created** — this file |

### `platform/windows`
| File | Change |
|------|--------|
| `README.md` | "Host-agnostic core" replaced with "Windows-native realization; platform integration permitted" |
| `agentic-coding-policy.json` | R003: updated from blanket dependency block to boundary compliance with precise rules |

### `platform/macos`
| File | Change |
|------|--------|
| `README.md` | "host-agnostic domain" replaced with "domain contracts are implementation-independent; services may integrate with platform framework" |
| `agentic-coding-policy.json` | R003: updated from blanket dependency block to boundary compliance with precise rules |

### `platform/ios`
| File | Change |
|------|--------|
| `README.md` | "host-agnostic domain" replaced with "domain contracts are implementation-independent; services may integrate with platform framework" |
| `agentic-coding-policy.json` | R003: updated from blanket dependency block to boundary compliance with precise rules |

## Next Priority

> The phase numbering model referenced above has been superseded by the repository realignment. The current priority is **repository realignment** (positioning this repo as the platform-agnostic authority). The next phase after realignment is **Agnostic Core design**. See [Roadmap Separation](roadmap_separation.md) for the current track structure.
