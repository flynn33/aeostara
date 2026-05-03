
# Diagnostic Chain Conformance

A conformant lifecycle has no orphan diagnostics. Root diagnostics reference themselves through `chainRootReference` and have no parent. Non-root diagnostics must reference an earlier parent. Every decision and audit event must link to a diagnostic reference.

Negative fixture cases must fail for missing parent, missing root, missing rule ID, decision without diagnostic, recovery step without diagnostic, and unreconstructable audit chain.
