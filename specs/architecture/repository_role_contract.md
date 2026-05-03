
# Repository Role Contract

Aeostara is platform-agnostic. Its role is to define the base semantics, contracts, algorithms, validation fixtures, and downstream handoff obligations for a self-healing JSON configuration engine.

## Authority Stack

```text
ASH Pattern System = fixed upstream semantic authority
Aeostara = platform-agnostic ASH-conformant base design
Windows/Mac/iOS repos = platform-specific downstream implementations
```

## Aeostara Owns

- JSON configuration semantics and canonical addressing.
- Semantic projection into the 9 ASH coordinates.
- ASH binding responsibilities and traceability.
- Diagnostic envelope, chain, audit, and rule-reference contracts.
- Recovery, policy, backup, execution, verification, rollback, fallback, containment, and safe-halt semantics.
- Platform-neutral fixture vectors and expected semantic outcomes.
- Downstream handoff requirements and acceptance templates.

## Aeostara Does Not Own

- Native Windows, Mac, or iOS implementation source.
- Platform-specific storage, file-system, security, notification, or packaging mechanics.
- Any modification or extension of ASH canonical semantics.

## Completion Rule

Base-design completion is independent of downstream platform source files. Completion is measured by ASH traceability, schema completeness, fixture conformance, diagnostic/audit integrity, safety lifecycle consistency, and handoff sufficiency.
