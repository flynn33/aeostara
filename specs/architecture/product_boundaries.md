# Aeostara / ASH / Forsetti Boundaries

## Aeostara (Product)

Aeostara is the product. It owns:
- Customer-facing behavior
- Contracts (11 data types)
- Config adapters (JSON for v0.1)
- Policy evaluation
- Repair planning
- Verification and rollback
- Audit trail
- Packaging and distribution model

## ASH Pattern System (Healing Kernel)

ASH provides the healing semantics. It owns:
- Encoded state model
- Drift distance semantics
- Correction concepts
- Confidence semantics (future)
- Pattern reasoning (future)
- Self-modeling concepts (future)

Aeostara v0.1 is ASH-inspired. Full ASH encoded-state mechanics are not yet implemented.

## Forsetti Framework (Host/Runtime)

Forsetti is the host/runtime framework. It owns:
- Runtime shell and lifecycle
- Module packaging
- Plugin system
- Entitlement
- UI composition
- Host services

## Repository Boundaries

In addition to the product/framework boundaries above, the repository structure enforces a separation between specification authority and platform implementation:

### Authority Repository (this repo)
- Owns: contracts, algorithms, interfaces, acceptance targets, compliance rules, architecture docs, shared fixtures, planning artifacts
- Defines: *what* Aeostara must do (behavior authority)
- Does not own: compilable source, platform toolchains, runtime dependencies

### Future Platform Repositories
- Own: native implementations, build infrastructure, CI pipelines, platform-specific testing, release packaging
- Define: *how* each platform realizes the specifications
- Must satisfy: all acceptance targets and compliance rules from the authority repo

See [Future Repo Split Plan](future_repo_split_plan.md) for the planned separation and [Repo Role and Scope](repo_role_and_scope.md) for full details.

## Non-Negotiable Boundary Rules

1. `main` branch specs remain code-agnostic and behavior-authoritative
2. Platform branches are native realization branches that may integrate with their platform's Forsetti framework
3. ASH stays framework-agnostic at the spec level
4. No core healing module may directly depend on UI code
5. Platform branch separation must not contaminate shared spec boundaries
6. Forsetti boundary rules apply to all platform branches:
   - No framework modification
   - No direct module-to-module communication
   - No direct OS communication
   - No module-owned UI
   - Framework-mediated I/O only
