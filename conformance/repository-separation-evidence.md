# Repository Separation Evidence

## Source Capture

| Source branch | Head | Tree | Commit count | Commit-set SHA-256 |
|---|---|---|---:|---|
| `platform/windows` | `0b5072181eb0576ba94018b5d7f945309bf2b8e5` | `eca549814828de3eeb75ef7464b83a182ebd02f6` | 13 | `6f3ec2ceb1a2fad826abc246841c4215694f93b34904faefde178d38e9f43fb1` |
| `platform/macos` | `b992a4b7f7b0847744a86bc50e4b946b1ef84119` | `edcd2e4c6edad9450bcec1db563540242e42c717` | 17 | `74f6bd7ba9f434c8beabb8ce3489ba6754ab76977865ef5e7b9bf5fef73fbb1a` |
| `platform/ios` | `0c931a7cbac349c6be93a6aeb4a253dd2268178f` | `2d45c54b7363f9e1205b597f814074c445e09025` | 18 | `959b01b0053f6634cdfe8004f5fcf6040d16d8eeb085d6ee2ff121ddabed6302` |

## Destination Import Verification

| Destination | Branch | Imported head | Imported tree | Commit count | Commit-set SHA-256 | Result |
|---|---|---|---|---:|---|---|
| `flynn33/Aeostara-Windows` | `main` | `0b5072181eb0576ba94018b5d7f945309bf2b8e5` | `eca549814828de3eeb75ef7464b83a182ebd02f6` | 13 | `6f3ec2ceb1a2fad826abc246841c4215694f93b34904faefde178d38e9f43fb1` | PASS |
| `flynn33/Aeostara-Mac-iOS` | `platform/macos` | `b992a4b7f7b0847744a86bc50e4b946b1ef84119` | `edcd2e4c6edad9450bcec1db563540242e42c717` | 17 | `74f6bd7ba9f434c8beabb8ce3489ba6754ab76977865ef5e7b9bf5fef73fbb1a` | PASS |
| `flynn33/Aeostara-Mac-iOS` | `platform/ios` | `0c931a7cbac349c6be93a6aeb4a253dd2268178f` | `2d45c54b7363f9e1205b597f814074c445e09025` | 18 | `959b01b0053f6634cdfe8004f5fcf6040d16d8eeb085d6ee2ff121ddabed6302` | PASS |

## Cutover and Recovery Verification

| Source branch | Archive tag retained | Bundle verified | Source branch deleted | Tag reconstruction | Bundle reconstruction | Result |
|---|---|---|---|---|---|---|
| `platform/windows` | PASS | PASS | PASS | PASS | PASS | PASS |
| `platform/macos` | PASS | PASS | PASS | PASS | PASS | PASS |
| `platform/ios` | PASS | PASS | PASS | PASS | PASS | PASS |
