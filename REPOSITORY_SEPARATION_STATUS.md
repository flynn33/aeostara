# Repository Separation Status

## Scope

Aeostara platform realizations are moving from source platform branches in `flynn33/aeostara` into permanent downstream repositories:

| Source branch | Destination repository | Destination branch | Captured head | Captured tree | Commit count |
|---|---|---|---|---|---:|
| `platform/windows` | `flynn33/Aeostara-Windows` | `main` | `0b5072181eb0576ba94018b5d7f945309bf2b8e5` | `eca549814828de3eeb75ef7464b83a182ebd02f6` | 13 |
| `platform/macos` | `flynn33/Aeostara-Mac-iOS` | `platform/macos` | `b992a4b7f7b0847744a86bc50e4b946b1ef84119` | `edcd2e4c6edad9450bcec1db563540242e42c717` | 17 |
| `platform/ios` | `flynn33/Aeostara-Mac-iOS` | `platform/ios` | `0c931a7cbac349c6be93a6aeb4a253dd2268178f` | `2d45c54b7363f9e1205b597f814074c445e09025` | 18 |

## Archive Tags and Bundles

| Branch | Source archive tag | Bundle path | Bundle SHA-256 |
|---|---|---|---|
| `platform/windows` | `archive/platform-windows-0b50721` | `/Volumes/NVME/Codex/Aeostara/closeout-evidence/bundles/aeostara-platform-windows-0b50721.bundle` | `de43e37717bb5eef6493018fcdd0b34e92ea534e14c9b8962d31d013f0fff8e9` |
| `platform/macos` | `archive/platform-macos-b992a4b` | `/Volumes/NVME/Codex/Aeostara/closeout-evidence/bundles/aeostara-platform-macos-b992a4b.bundle` | `408c553b8a2e1536898b46d3438c69111236dee6502d02ca3a9c6f1b4afe6c5f` |
| `platform/ios` | `archive/platform-ios-0c931a7` | `/Volumes/NVME/Codex/Aeostara/closeout-evidence/bundles/aeostara-platform-ios-0c931a7.bundle` | `ae2ff2d422359919b11a7374ce7b6a90bd779e73c7692e7329f77808b604a680` |

## Destination Import Tags

| Destination | Import tag |
|---|---|
| `flynn33/Aeostara-Windows` | `import/platform-windows-0b50721` |
| `flynn33/Aeostara-Mac-iOS` | `import/platform-macos-b992a4b` |
| `flynn33/Aeostara-Mac-iOS` | `import/platform-ios-0c931a7` |

## Source Cutover and Recovery

| Branch | Source branch deleted | Archive tag retained | Bundle verified | Reconstruction result |
|---|---|---|---|---|
| `platform/windows` | PASS | PASS | PASS | PASS |
| `platform/macos` | PASS | PASS | PASS | PASS |
| `platform/ios` | PASS | PASS | PASS | PASS |

## Current Judgment

Final judgment: `CONFORMANT`.
