#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import REQUIRED_FIXTURE_FILES, load_json, load_schemas, print_result, repo_root_from_arg, validate_instance

REQUIRED_EXPECTED = [
    "diagnosticKind",
    "stateClass",
    "recoveryCategory",
    "mustEmitDiagnostics",
    "mustEmitAuditEvents",
    "mustMutate",
    "requiredSchemaOutputs",
]


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    schemas, schema_failures = load_schemas(root)
    failures = list(schema_failures)
    fixture_dir = root / "fixtures" / "conformance"
    manifest = fixture_dir / "manifest.json"
    if not manifest.is_file():
        failures.append("missing fixtures/conformance/manifest.json")
    else:
        try:
            listed = set(load_json(manifest).get("fixtureFiles", []))
            missing_from_manifest = [name for name in REQUIRED_FIXTURE_FILES if name not in listed]
            for name in missing_from_manifest:
                failures.append(f"fixture manifest missing {name}")
        except Exception as exc:  # noqa: BLE001
            failures.append(f"invalid fixture manifest: {exc}")
    for name in REQUIRED_FIXTURE_FILES:
        path = fixture_dir / name
        if not path.is_file():
            failures.append(f"missing fixture file: fixtures/conformance/{name}")
            continue
        try:
            payload = load_json(path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"invalid fixture JSON {name}: {exc}")
            continue
        vectors = payload.get("vectors")
        if not isinstance(vectors, list) or not vectors:
            failures.append(f"{name}: vectors must be a non-empty list")
            continue
        for index, vector in enumerate(vectors):
            prefix = f"{name}.vectors[{index}]"
            for key in ["fixtureID", "category", "sourceReferences", "input", "expected", "negativeAssertions"]:
                if key not in vector:
                    failures.append(f"{prefix}: missing {key}")
            expected = vector.get("expected", {})
            for key in REQUIRED_EXPECTED:
                if key not in expected:
                    failures.append(f"{prefix}.expected: missing {key}")
            if expected.get("mustEmitDiagnostics") is not True:
                failures.append(f"{prefix}: mustEmitDiagnostics must be true")
            if expected.get("mustEmitAuditEvents") is not True:
                failures.append(f"{prefix}: mustEmitAuditEvents must be true")
            outputs = expected.get("requiredSchemaOutputs", [])
            if not isinstance(outputs, list) or not outputs:
                failures.append(f"{prefix}: expected.requiredSchemaOutputs must be non-empty")
                continue
            for out_index, output in enumerate(outputs):
                schema_name = output.get("schema") if isinstance(output, dict) else None
                instance = output.get("instance") if isinstance(output, dict) else None
                if schema_name not in schemas:
                    failures.append(f"{prefix}.requiredSchemaOutputs[{out_index}]: unknown schema {schema_name}")
                    continue
                failures.extend(
                    f"{prefix}.requiredSchemaOutputs[{out_index}] {issue}"
                    for issue in validate_instance(instance, schemas[schema_name], schemas)
                )
    return print_result("fixture validation", failures, "PASS: conformance fixtures contain expected schema-valid outputs.")


if __name__ == "__main__":
    raise SystemExit(main())
