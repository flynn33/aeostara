
# ASH Authority Traceability Matrix

| ASH source area | Aeostara response | Downstream obligation |
|---|---|---|
| State space | `AshState`, `ash_state_space_binding.md` | Use all 9 coordinates |
| Codeword set | `CanonicalCodewordSet`, `canonical_codeword_set_binding.md` | Use exactly 16 codewords |
| Transformation | `CodewordTransformation`, transformation algorithm | Apply XOR-by-codeword |
| Admissibility | `AdmissibilityResult` | Classify deterministically |
| Diagnostics | `DiagnosticEnvelope`, `DiagnosticChain` | Emit linked diagnostics |
| Classification | `SystemStateClass` | Preserve class mapping |
| Recoverability | `RecoveryCategory`, `RecoveryPlan` | Preserve deterministic categories |
| Fallback | `FallbackDecision` | Registry-driven selection |
| Containment/safe halt | `ContainmentDecision`, `SafeHaltDecision` | Safe halt is terminal |
| Realm/transition/topology/axiom/generation | Binding docs and schemas | Implement without redefining semantics |
