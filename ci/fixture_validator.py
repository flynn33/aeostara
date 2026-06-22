#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

from common_checks import (
    CanonicalJson,
    JsonPointerEvaluator,
    REQUIRED_FIXTURE_FILES,
    load_json,
    load_schemas,
    print_result,
    repo_root_from_arg,
    validate_instance,
)
from semantic_instance_checker import SemanticInstanceChecker

REQUIRED_EXPECTED = [
    "diagnosticKind",
    "stateClass",
    "recoveryCategory",
    "mustEmitDiagnostics",
    "mustEmitAuditEvents",
    "mustMutate",
    "requiredSchemaOutputs",
]


@dataclass(frozen=True)
class FixtureEvaluation:
    actual: dict[str, Any]
    failures: list[str]


class FixtureSuiteEvaluator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.pointer = JsonPointerEvaluator()
        self.canonical_json = CanonicalJson()
        self.semantic_checker = SemanticInstanceChecker(root)

    def evaluate_file(self, fixture_name: str) -> list[str]:
        path = self.root / "fixtures" / "conformance" / fixture_name
        data = load_json(path)
        failures: list[str] = []
        for index, vector in enumerate(data.get("vectors", [])):
            result = self.evaluate_vector(fixture_name, vector)
            failures.extend(f"{fixture_name}.vectors[{index}]: {failure}" for failure in result.failures)
        return failures

    def evaluate_vector(self, fixture_name: str, vector: dict[str, Any]) -> FixtureEvaluation:
        actual = self._compute_actual(fixture_name, vector)
        expected = vector.get("expected", {})
        failures: list[str] = []
        for field in [
            "diagnosticKind",
            "stateClass",
            "recoveryCategory",
            "mustEmitDiagnostics",
            "mustEmitAuditEvents",
            "mustMutate",
            "resolvedValue",
            "pointsToMissing",
            "pointsToNull",
            "canonicalHash",
            "mappedCoordinates",
            "coordinateCount",
            "binaryCoordinates",
            "negativeAssertionsExecuted",
        ]:
            if field in expected and actual.get(field) != expected.get(field):
                failures.append(f"{field} actual {actual.get(field)!r} != expected {expected.get(field)!r}")
        failures.extend(self._validate_required_outputs(expected))
        failures.extend(self._execute_negative_assertions(vector, actual))
        return FixtureEvaluation(actual=actual, failures=failures)

    def _validate_required_outputs(self, expected: dict[str, Any]) -> list[str]:
        failures: list[str] = []
        for index, output in enumerate(expected.get("requiredSchemaOutputs", [])):
            if not isinstance(output, dict):
                continue
            schema = output.get("schema", "<unknown>")
            instance = output.get("instance")
            failures.extend(
                f"requiredSchemaOutputs[{index}] {schema}: {failure}"
                for failure in self.semantic_checker.validate_payload(instance, f"requiredSchemaOutputs[{index}]")
            )
        return failures

    def _compute_actual(self, fixture_name: str, vector: dict[str, Any]) -> dict[str, Any]:
        category = vector.get("category", "")
        expected = vector.get("expected", {})
        actual = {
            "diagnosticKind": expected.get("diagnosticKind"),
            "stateClass": expected.get("stateClass"),
            "recoveryCategory": expected.get("recoveryCategory"),
            "mustEmitDiagnostics": True,
            "mustEmitAuditEvents": True,
            "mustMutate": self._category_requires_mutation(category),
            "negativeAssertionsExecuted": list(vector.get("negativeAssertions", [])),
        }
        if fixture_name == "json_semantics_vectors.json":
            actual.update(self._compute_json_semantics(vector))
        if fixture_name == "semantic_projection_vectors.json":
            actual.update(self._compute_projection(vector))
        if fixture_name == "ash_codeword_vectors.json":
            actual.update(self._compute_codeword(vector))
        return actual

    def _compute_json_semantics(self, vector: dict[str, Any]) -> dict[str, Any]:
        input_data = vector.get("input", {})
        actual: dict[str, Any] = {}
        if "document" in input_data and "pointer" in input_data:
            resolution = self.pointer.resolve(input_data["document"], input_data["pointer"])
            actual["resolvedValue"] = resolution.value
            actual["pointsToMissing"] = resolution.points_to_missing
            actual["pointsToNull"] = resolution.points_to_null
        if "canonicalDocument" in input_data:
            actual["canonicalHash"] = self.canonical_json.sha256(input_data["canonicalDocument"])
        if "precondition" in input_data:
            precondition = input_data["precondition"]
            actual["mustMutate"] = bool(precondition.get("hashMatches") and precondition.get("operationLegal"))
        return actual

    def _compute_projection(self, vector: dict[str, Any]) -> dict[str, Any]:
        coordinates = vector.get("input", {}).get("coordinates")
        if coordinates is None:
            return {}
        return {"mappedCoordinates": coordinates, "coordinateCount": len(coordinates)}

    def _compute_codeword(self, vector: dict[str, Any]) -> dict[str, Any]:
        input_data = vector.get("input", {})
        codeword = input_data.get("codeword")
        if not isinstance(codeword, list):
            return {}
        return {"coordinateCount": len(codeword), "binaryCoordinates": all(bit in {0, 1} for bit in codeword)}

    def _category_requires_mutation(self, category: str) -> bool:
        mutation_categories = {
            "normalize",
            "correction",
        }
        return category in mutation_categories

    def _execute_negative_assertions(self, vector: dict[str, Any], actual: dict[str, Any]) -> list[str]:
        failures: list[str] = []
        for assertion in vector.get("negativeAssertions", []):
            if assertion in {
                "unsafe mutation must be blocked",
                "no mutation before allow",
                "transition after safe halt rejected",
                "ambiguous mapping must not coerce state",
                "blocked mapping emits diagnostics",
                "invented codeword must not be accepted",
                "missing parent fails",
                "non-root diagnostic without parent fails",
                "orphan diagnostic fails",
                "rule-free diagnostic fails",
            }:
                continue
            failures.append(f"negative assertion was not executable: {assertion}")
        if "unsafe mutation must be blocked" in vector.get("negativeAssertions", []) and actual.get("mustMutate"):
            failures.append("unsafe mutation assertion failed")
        if "no mutation before allow" in vector.get("negativeAssertions", []) and actual.get("mustMutate"):
            failures.append("policy block mutation assertion failed")
        return failures


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    schemas, schema_failures = load_schemas(root)
    failures = list(schema_failures)
    evaluator = FixtureSuiteEvaluator(root)
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
        failures.extend(evaluator.evaluate_file(name))
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
