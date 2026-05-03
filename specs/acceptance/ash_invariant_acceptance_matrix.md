
# ASH Invariant Acceptance Matrix

| Category | Required families | Required fixtures |
|---|---|---|
| Algebraic/State Conformance | INV-STATE, INV-ADMISSIBILITY, INV-CODEWORD | ash_codeword_vectors, state_admissibility_vectors |
| Recovery/Fallback/Containment Conformance | INV-RECOVERY | recovery_escalation_vectors, safe_halt_terminal_vectors |
| Diagnostics Conformance | INV-DIAG, INV-AXIOM | diagnostic_chain_vectors |
| Generation/Materialization-Boundary Conformance | INV-PLAN, INV-BOUNDARY | end_to_end_healing_vectors |
| Contract/Module Conformance | INV-REALM, INV-TRANS, INV-TOPO | semantic_projection_vectors |
