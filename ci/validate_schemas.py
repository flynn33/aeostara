#!/usr/bin/env python3
"""
Aeostara Contract Validator
Validates required contract schemas and legacy-status semantics.
"""

import json
import os
import sys
from typing import Dict, List, Tuple


REQUIRED_AUTHORITATIVE_SCHEMAS = [
    "ObservedSystemState.schema.json",
    "DesiredSystemIntent.schema.json",
    "AshSemanticState.schema.json",
    "StateValidityDiagnostic.schema.json",
    "SystemStateClass.schema.json",
    "RecoveryCategory.schema.json",
    "RecoveryPlan.schema.json",
    "FallbackDecision.schema.json",
    "ContainmentDecision.schema.json",
    "SafeHaltDecision.schema.json",
    "RollbackPlan.schema.json",
    "VerificationResult.schema.json",
    "AuditEvent.schema.json",
    "ModuleManifest.schema.json",
]

LEGACY_NON_AUTHORITATIVE_SCHEMAS = [
    "EncodedState.schema.json",
    "ObservedState.schema.json",
    "DesiredState.schema.json",
    "DriftEvent.schema.json",
    "RepairAction.schema.json",
    "RepairPlan.schema.json",
    "Invariant.schema.json",
]


def load_json(filepath: str) -> Tuple[bool, Dict, str]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return True, json.load(f), "OK"
    except json.JSONDecodeError as exc:
        return False, {}, f"Invalid JSON: {exc}"
    except OSError as exc:
        return False, {}, f"Read error: {exc}"


def validate_base_schema_fields(schema: Dict) -> Tuple[bool, str]:
    required = ["$schema", "title", "type"]
    missing = [key for key in required if key not in schema]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, "OK"


def validate_authoritative_schema(filename: str, schema: Dict) -> Tuple[bool, str]:
    if schema.get("x-status") == "legacy-non-authoritative":
        return False, "Authoritative schema incorrectly marked as legacy"
    return True, "OK"


def validate_legacy_schema(filename: str, schema: Dict) -> Tuple[bool, str]:
    if schema.get("x-status") != "legacy-non-authoritative":
        return False, "Legacy schema must set x-status=legacy-non-authoritative"
    replacement = schema.get("x-replacement")
    if not replacement:
        return False, "Legacy schema missing x-replacement"
    return True, "OK"


def ensure_presence(contracts_dir: str, filenames: List[str]) -> List[str]:
    missing = []
    for name in filenames:
        if not os.path.isfile(os.path.join(contracts_dir, name)):
            missing.append(name)
    return missing


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    contracts_dir = os.path.join(repo_root, "specs", "contracts")

    if not os.path.isdir(contracts_dir):
        print(f"FAIL: contracts directory not found: {contracts_dir}")
        return 1

    failures = 0

    missing_authoritative = ensure_presence(contracts_dir, REQUIRED_AUTHORITATIVE_SCHEMAS)
    missing_legacy = ensure_presence(contracts_dir, LEGACY_NON_AUTHORITATIVE_SCHEMAS)

    if missing_authoritative:
        print("FAIL: missing required authoritative schemas:")
        for name in missing_authoritative:
            print(f"  - {name}")
        failures += len(missing_authoritative)

    if missing_legacy:
        print("FAIL: missing required legacy-marked schemas:")
        for name in missing_legacy:
            print(f"  - {name}")
        failures += len(missing_legacy)

    all_targets = REQUIRED_AUTHORITATIVE_SCHEMAS + LEGACY_NON_AUTHORITATIVE_SCHEMAS

    print(f"Validating {len(all_targets)} targeted schemas...")

    for filename in all_targets:
        filepath = os.path.join(contracts_dir, filename)
        if not os.path.isfile(filepath):
            continue

        ok, schema, message = load_json(filepath)
        if not ok:
            print(f"  [FAIL] {filename}: {message}")
            failures += 1
            continue

        ok, message = validate_base_schema_fields(schema)
        if not ok:
            print(f"  [FAIL] {filename}: {message}")
            failures += 1
            continue

        if filename in REQUIRED_AUTHORITATIVE_SCHEMAS:
            ok, message = validate_authoritative_schema(filename, schema)
        else:
            ok, message = validate_legacy_schema(filename, schema)

        if ok:
            print(f"  [PASS] {filename}: {message}")
        else:
            print(f"  [FAIL] {filename}: {message}")
            failures += 1

    if failures:
        print(f"\nFAIL: {failures} schema validation issue(s) detected.")
        return 1

    print("\nPASS: contract schemas satisfy remediation validation gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
