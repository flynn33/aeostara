
# Downstream Platform Status Matrix

This matrix records the downstream repository split. It is not an active Aeostara base-design completion gate.

Aeostara completion does not require native Windows, Mac, or iOS source files. Platform repositories consume Aeostara and report their own implementation status using the handoff templates under `templates/platform_repo/`.

| Downstream repo | Aeostara version pin | Required adapters mapped | Required contracts implemented | Fixtures passed | Deviations logged | Judgment |
|---|---|---:|---:|---:|---:|---|
| `flynn33/Aeostara-Windows:main` | `v1.0.0` | Destination-owned | Destination-owned | Destination-owned | Destination-owned | Runtime judgment is independent of base release |
| `flynn33/Aeostara-Mac-iOS:platform/macos` | `v1.0.0` | Destination-owned | Destination-owned | Destination-owned | Destination-owned | Runtime judgment is independent of base release |
| `flynn33/Aeostara-Mac-iOS:platform/ios` | `v1.0.0` | Destination-owned | Destination-owned | Destination-owned | Destination-owned | Runtime judgment is independent of base release |

A downstream repo may record platform limitations as caveats or deviations. It may not redefine Aeostara base semantics.
