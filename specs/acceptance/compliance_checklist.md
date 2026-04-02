# Root Specification Compliance Checklist

> This checklist tracks root-level specification compliance. Platform-specific build, test, and toolchain verification is the responsibility of each platform implementation (currently branches, planned as separate repos).

## Root Specifications (main branch)
- [x] 11 contract JSON schemas present and valid
- [x] 9 algorithm pseudo code files present
- [x] 5 interface pseudo code files present
- [x] Architecture documents present
- [x] Acceptance targets documented
- [x] Compliance rules documented
- [x] Root governance policy is platform-agnostic and language-agnostic
- [x] No compilable source code on main branch

## Branch / Repo Structure
- [x] `main` branch contains only specifications
- [x] `platform/windows` branch contains Windows implementation
- [x] `platform/macos` branch contains macOS implementation
- [x] `platform/ios` branch contains iOS implementation
- [x] Branch responsibilities documented (see branching_strategy.md)
- [x] Merge policy documented (main -> platform, one-way)
- [x] Future repo split plan documented (see future_repo_split_plan.md)

## Shared Behavioral Requirements (all platforms)
- [x] 5 acceptance scenarios defined (valid config, parse error, policy block, repair, rollback)
- [x] Deterministic behavior required (same input = same output)
- [x] Backup before mutation required
- [x] Rollback on verification failure required
- [x] Audit trail required
- [x] Policy gating required
- [x] No Python in shipped product
- [x] No YAML in shipped product
- [x] Native-only shipped binary

## Platform Verification Status
- [x] Windows: Reference implementation, locally proven (build + test)
- [ ] macOS: Source present, build unverified (deferred to platform repo)
- [ ] iOS: Source present, build unverified (deferred to platform repo)
- [ ] CI runner proof obtained for any platform

## Shared Test Fixtures
- [x] All 6 fixture files present on main branch
- [ ] Fixture identity verified across all platform branches
