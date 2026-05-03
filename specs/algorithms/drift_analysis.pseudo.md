# Surface Difference Evidence

This is the authoritative downstream algorithm for Aeostara surface-difference evidence under the ASH Pattern System.

It binds observed-vs-intent comparison to ASH-aligned diagnostics, classification, and recovery-category selection.

## produce_drift_evidence(observed_state, desired_intent, diagnostic) -> list

```text
FUNCTION produce_drift_evidence(observed_state, desired_intent, diagnostic):
  surface_differences = deterministic_diff(observed_state.rawState, desired_intent.intentState)
  evidence = []

  FOR EACH difference IN surface_differences:
    evidence.append(DriftEventEvidence(
      evidenceID = stable_id(difference.path, diagnostic.diagnosticID),
      keyPath = difference.path,
      type = difference.kind,
      observedValue = difference.observed,
      desiredValue = difference.desired,
      description = "Surface evidence associated with ASH diagnostic",
      diagnosticReferences = [diagnostic.diagnosticID]
    ))

  RETURN evidence
END FUNCTION
```

## Authority Constraint

Surface evidence is authoritative for Aeostara's downstream evidence layer. ASH-aligned diagnostics remain authoritative for semantic state validity and classification.
