
# ASH Invariant Coverage Map

Baseline: `ASH Pattern System main@e123f5d7fdbb381179971f721a3292c31eb1cbc2`

## Upstream ASH Source

- `specs/verification/conformance-categories.md`
- `specs/verification/invariant-spec.md`

## Aeostara Binding Responsibility

Aeostara binds every required invariant family to a base-design artifact, contract, and fixture family. All 5 ASH conformance categories are required.

## Downstream Platform Obligation

Downstream platform repositories must run the Aeostara fixture vectors and produce conformance reports for every category below. A platform limitation is recorded as a caveat or deviation, not as a change to ASH or Aeostara semantics.

## Diagnostics and Audit Requirements

Invariant failures, blocked checks, and rejected downstream claims must emit diagnostic references and audit events that reconstruct the evaluated invariant category and source rule.

## Conformance Tests

The fixture evidence column identifies the required platform-neutral vectors for each category.

| ASH conformance category | Invariant families | Aeostara bindings | Fixture evidence |
|---|---|---|---|
| Algebraic/State Conformance | `INV-STATE`, `INV-ADMISSIBILITY`, `INV-CODEWORD` | `ash_state_space_binding.md`, `canonical_codeword_set_binding.md`, `codeword_transformation_binding.md`, `state_admissibility_binding.md` | `ash_codeword_vectors.json`, `state_admissibility_vectors.json` |
| Recovery/Fallback/Containment Conformance | `INV-RECOVERY` | `recoverability_binding.md`, `fallback_policy_registry_binding.md`, `containment_safe_halt_binding.md` | `recovery_escalation_vectors.json`, `policy_block_vectors.json`, `backup_rollback_vectors.json`, `safe_halt_terminal_vectors.json` |
| Diagnostics Conformance | `INV-DIAG`, `INV-AXIOM` | `state_validity_diagnostic_binding.md`, `axiom_evaluator_binding.md` | `diagnostic_chain_vectors.json` |
| Generation/Materialization-Boundary Conformance | `INV-PLAN`, `INV-BOUNDARY` | `generation_materialization_boundary.md` | `end_to_end_healing_vectors.json` |
| Contract/Module Conformance | `INV-REALM`, `INV-TRANS`, `INV-TOPO` | `realm_identity_binding.md`, `transition_registry_binding.md`, `topology_generator_binding.md` | `semantic_projection_vectors.json`, `ash_codeword_vectors.json` |

All 5 ASH conformance categories are required. Partial coverage is not sufficient.
