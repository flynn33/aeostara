
# Downstream Platform Repository Contract

Downstream platform repositories implement Aeostara. They do not redefine Aeostara.

## Required Downstream Obligations

Each Windows, Mac, and iOS repo must:

1. Pin the Aeostara base-design version or commit it implements.
2. Map every required Aeostara interface to a native module.
3. Implement all required contracts without changing field meanings.
4. Run the platform-neutral conformance fixture vectors and record expected outputs.
5. Produce diagnostics that conform to `DiagnosticEnvelope`, `DiagnosticReference`, and `DiagnosticChain`.
6. Emit audit events that reconstruct the lifecycle.
7. Document platform limitations as deviations or caveats, not semantic changes.
8. Preserve ASH authority and Aeostara base-design authority.

## Prohibited Downstream Behavior

- Inventing local rule-ID formats.
- Extending the ASH codeword set.
- Treating surface JSON diffs as semantic truth.
- Mutating configuration before policy, backup, and verification obligations are met.
- Bypassing fallback, containment, or safe halt without diagnostics.
