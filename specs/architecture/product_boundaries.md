# Aeostara Product Boundaries

## Aeostara (Product)

Aeostara is the product — a self-healing and safe-failure / fallback system that developers incorporate into their software. It owns:
- Customer-facing behavior
- Contracts (11 data types)
- Config adapters (JSON for v0.1)
- Policy evaluation
- Repair planning
- Verification and rollback
- Audit trail
- Packaging and distribution model

## ASH Pattern System (Core Subsystem)

The ASH Pattern System is **part of Aeostara Core**. It is not a separate peer layer. It provides the core healing semantics within Aeostara:
- Encoded state model
- Drift distance semantics
- Correction concepts
- Confidence semantics (future)
- Pattern reasoning (future)
- Self-modeling concepts (future)

The ASH Pattern System is language-agnostic and platform-agnostic in its implementation within Aeostara Core. Aeostara v0.1 incorporates foundational ASH Pattern System concepts. Full ASH Pattern System formalization is deferred to a future phase.

## Repository Boundaries

The repository structure enforces a separation between specification authority and platform implementation:

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
2. The ASH Pattern System stays language-agnostic and platform-agnostic at the spec level
3. No core healing module may directly depend on UI code
4. Platform branch separation must not contaminate shared spec boundaries
5. Platform branches are native realization branches that implement shared behavior using their platform's native toolchain
