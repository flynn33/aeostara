# Policy Gate Lifecycle

## Purpose and Authority Source

This active algorithm defines deterministic Aeostara base-design behavior for `policy_gate_lifecycle.pseudo.md`. Authority flows from the ASH Pattern System baseline through the frozen Aeostara contracts, ASH bindings, conformance fixtures, and lifecycle documents.

- The fixed lifecycle order is Observe, Normalize, Project, Diagnose, Classify, RecoveryCategory, Plan, PolicyGate, VerificationPlan, Backup, Execute, Verify, then Rollback, Fallback, Containment, SafeHalt, and Result as applicable.

## Inputs and Outputs

- Inputs are the schema-valid contract objects named by the companion interface, fixture, or lifecycle phase.
- Outputs are schema-valid contract objects from `specs/contracts/`, plus linked `DiagnosticEnvelope`, `DiagnosticChain`, `AuditEvent`, and `AuditChain` evidence.
- Serialized outputs must not add fields, enum values, lifecycle phases, ASH coordinates, or alternate address forms.

## Preconditions

- Every input has already passed JSON Schema validation and cross-schema semantic validation.
- Rule references resolve to ASH baseline or Aeostara binding paths.
- Planning and dry-run invocations receive immutable input snapshots and cannot hold mutation capability.
- Policy, backup, execution, verification, rollback, fallback, containment, and safe-halt phases run only when the immediately preceding lifecycle decision permits them.

## Deterministic Ordering and Tie-Breaking

- Sort unordered identifiers lexicographically by UTF-8 code-unit sequence.
- Preserve array order when arrays are part of the source contract value.
- Order ASH coordinates as b0 through b8.
- When equal-cost recovery or fallback candidates exist, choose the candidate with the smallest canonical serialized representation and record the tie in diagnostics.
- Hash identities use SHA-256 over canonical JSON with nondeterministic creation time excluded where the contract identity rules require it.

## Complete Pseudocode

```text
FUNCTION run_policy_gate_lifecycle(input, lifecycleContext) -> contractOutput
  ASSERT input is schema-valid and semantically valid
  diagnosticChain = lifecycleContext.diagnosticChain
  auditChain = lifecycleContext.auditChain
  IF required evidence is missing:
    envelope = DiagnosticEnvelope(kind=STATE_VALIDITY, severity=ERROR, outcome=BLOCKED)
    diagnosticChain = append_diagnostic(diagnosticChain, envelope)
    auditChain = append_audit(auditChain, phase=current_phase, outcome=BLOCKED)
    RETURN blocked contract output linked to diagnosticChain and auditChain
  IF evidence is malformed or violates a frozen semantic rule:
    envelope = DiagnosticEnvelope(kind=STATE_VALIDITY, severity=CRITICAL, outcome=FAILED)
    diagnosticChain = append_diagnostic(diagnosticChain, envelope)
    auditChain = append_audit(auditChain, phase=current_phase, outcome=FAILED)
    RETURN failed contract output linked to diagnosticChain and auditChain
  normalized = canonicalize_inputs_without_mutation(input)
  decision = evaluate_domain_rule_for_this_algorithm(normalized)
  IF decision is AMBIGUOUS:
    envelope = DiagnosticEnvelope(kind=MAPPING, severity=ERROR, outcome=AMBIGUOUS)
    RETURN ambiguous contract output with no mutation and linked evidence
  IF decision is TERMINAL:
    envelope = DiagnosticEnvelope(kind=SAFE_HALT, severity=CRITICAL, outcome=TERMINAL)
    RETURN terminal contract output that forbids further normal execution
  output = build_schema_valid_contract_output(decision)
  output = attach_diagnostic_and_audit_references(output, diagnosticChain, auditChain)
  RETURN output
END FUNCTION
```

## Outcomes

- SUCCESS returns the deterministic contract output and emits ordered diagnostic and audit evidence.
- NO_ACTION returns no executable recovery step, `wouldMutate=false`, `requiresPolicyGate=false`, and `requiresBackup=false` where RecoveryPlan is produced.
- BLOCKED returns no unauthorized mutation and selects the next fixed escalation decision.
- AMBIGUOUS preserves every candidate and blocks coerced mapping or execution.
- FAILED records root cause evidence and fails closed.
- TERMINAL safe halt forbids subsequent mutation and normal execution.

## DiagnosticEnvelope and Chain Linkage

Every material decision, rejected precondition, BLOCKED result, AMBIGUOUS result, FAILED result, rollback path, fallback path, containment boundary, and terminal safe halt creates or propagates a `DiagnosticEnvelope`. Parent links reference earlier diagnostics only, and every envelope includes a valid rule reference and source reference.

## AuditEvent Ordering

Each completed phase appends one `AuditEvent` with a one-based contiguous sequence. The event references the active diagnostic chain and records the lifecycle phase, selected outcome, and non-sensitive evidence. Audit persistence failure is reported as FAILED and cannot be suppressed.

## Side-Effect Classification

Planning, normalization, projection, diagnosis, classification, materialization planning, verification-plan generation, and dry-run execution have no side effects. Approved mutation is allowed only in execution, platform mutation, rollback, and documented persistence phases after policy and backup gates pass.

## Postconditions

- Contract outputs validate against the frozen schema inventory.
- Contract hashes remain unchanged.
- No platform-native source is introduced into agnostic `main`.
- DiagnosticChain and AuditChain evidence reconstruct the same lifecycle outcome.
- Repeating the algorithm with identical immutable inputs produces byte-identical canonical output except for fields explicitly supplied by deterministic input.

## Negative Cases

- Missing evidence produces BLOCKED rather than fabricated values.
- Malformed evidence produces FAILED rather than success.
- Invalid policy, backup, audit, execution, verification, or rollback evidence fails closed.
- Mutation during planning or dry run is rejected.
- Unsupported ASH coordinates, JSON dot paths, missing/null conflation, and non-SHA-256 identities are rejected.

## Fixture References

- `fixtures/conformance/json_semantics_vectors.json`
- `fixtures/conformance/semantic_projection_vectors.json`
- `fixtures/conformance/ash_codeword_vectors.json`
- `fixtures/conformance/recovery_escalation_vectors.json`
- `fixtures/conformance/end_to_end_healing_vectors.json`

## Downstream Implementation Obligations

Swift and C++ implementations must preserve operation order, side-effect boundaries, contract fields, enum values, JSON Pointer semantics, ASH coordinate order, DiagnosticEnvelope creation, AuditEvent ordering, and fail-closed behavior. Platform code may implement native mechanics but may not redefine Aeostara or ASH semantics.
