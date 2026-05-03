
# Platform Implementation Boundary

Aeostara specifies behavior; platform repos implement mechanics.

| Concern | Aeostara base design | Platform repositories |
|---|---|---|
| ASH semantics | Bind to fixed upstream ASH sources | Consume without redefinition |
| JSON semantics | Define pointer addressing, canonicalization, preconditions | Implement parser/storage details |
| Diagnostics | Define envelopes, chains, rule references | Emit conforming records |
| Policy | Define decision contract and gate lifecycle | Connect native policy sources |
| Backup | Define backup record/result semantics | Create platform-native backup artifacts |
| Execution | Define approved-step lifecycle | Mutate platform resources safely |
| Verification | Define plan/result semantics | Run native checks and report results |
| Rollback | Define triggers and result semantics | Restore from backups |
| Fallback/containment/halt | Define deterministic escalation | Enforce native restrictions and halt behavior |

No platform-native source code is required or accepted as an Aeostara base-design completion artifact.
