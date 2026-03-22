# Repository Branch Drift Matrix

Date: 2026-03-22
Status: Post-alignment correction pass

## Branch Status

| Branch | Purpose | Old Wording Issue | Corrected Wording | Residual Drift |
|--------|---------|-------------------|-------------------|----------------|
| `main` | Code-agnostic specs | "host-agnostic core" applied too broadly; implied platform branches must preserve implementation agnosticism | Code-agnostic and behavior-authoritative; platform branches are native realization branches | None |
| `platform/windows` | Windows-native realization | R003 "No Forsetti Dependency" blanket-blocked valid native integration; "host-agnostic core" language | Forsetti Boundary Compliance with precise rules; Windows-native integration permitted | None |
| `platform/macos` | macOS-native realization | R003 "No Forsetti Dependency" blanket-blocked valid native integration; "host-agnostic domain" language | Forsetti Boundary Compliance; macOS-native integration permitted at services layer | Build/test proof deferred (Windows PC) |
| `platform/ios` | iOS-native realization | R003 "No Forsetti Dependency" blanket-blocked valid native integration; "host-agnostic domain" language | Forsetti Boundary Compliance; iOS-native integration permitted at services layer | Build/test proof deferred (Windows PC) |

## Files Changed Per Branch

### `main`
| File | Change |
|------|--------|
| `README.md` | Branch model: "native realization branches" added; compliance: "host-agnostic core" → code-agnostic specs |
| `specs/architecture/compliance_rules.md` | Rule 5: "Host-agnostic core" → "Code-agnostic specs"; Rule 6: "Interface-based Forsetti" → "Forsetti boundary compliance" |
| `specs/architecture/product_boundaries.md` | "Aeostara Core stays host-agnostic" → "`main` specs remain code-agnostic; platform branches are native realization branches" |
| `specs/architecture/branching_strategy.md` | Added "native realization branches" section explaining platform branches need not preserve `main`'s abstraction posture |
| `specs/architecture/native_target_architecture.md` | Added "Shared Specs vs Native Realization" section |
| `specs/architecture/branch_native_realization_clarification.md` | **Created** — locks corrected baseline |
| `specs/architecture/repo_branch_drift_matrix.md` | **Created** — this file |

### `platform/windows`
| File | Change |
|------|--------|
| `README.md` | "Host-agnostic core" → "Windows-native realization; Forsetti integration permitted" |
| `agentic-coding-policy.json` | R003: "No Forsetti Dependency" → "Forsetti Boundary Compliance" with precise rules |

### `platform/macos`
| File | Change |
|------|--------|
| `README.md` | "host-agnostic domain" → "domain contracts are Forsetti-independent; services may integrate with macOS Forsetti framework" |
| `agentic-coding-policy.json` | R003: "No Forsetti Dependency" → "Forsetti Boundary Compliance" with precise rules |

### `platform/ios`
| File | Change |
|------|--------|
| `README.md` | "host-agnostic domain" → "domain contracts are Forsetti-independent; services may integrate with iOS Forsetti framework" |
| `agentic-coding-policy.json` | R003: "No Forsetti Dependency" → "Forsetti Boundary Compliance" with precise rules |

## Next Priority

**Phase 7 — Windows Completion and Release Hardening** remains the active priority after this alignment pass.
