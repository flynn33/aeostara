#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from common_checks import CanonicalJson, load_json, print_result, repo_root_from_arg, validate_schemas_and_examples


class SemanticInstanceChecker:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.canonical_json = CanonicalJson()

    def validate(self) -> list[str]:
        failures = validate_schemas_and_examples(self.root)
        for path in sorted((self.root / "fixtures" / "schema_examples").glob("*.example.json")):
            failures.extend(self.validate_example(path.relative_to(self.root)))
        return failures

    def validate_example(self, relative_path: Path) -> list[str]:
        path = self.root / relative_path
        data = load_json(path)
        failures = self.validate_payload(data, str(relative_path))
        if path.name == "MappingResult.example.json":
            failures.extend(self._validate_mapping_result(data))
        if path.name == "SemanticProjectionSpec.example.json":
            failures.extend(self._validate_projection_spec(data))
        if path.name == "DiagnosticChain.example.json":
            failures.extend(self._validate_diagnostic_chain(data))
        if path.name == "AuditChain.example.json":
            failures.extend(self._validate_audit_chain(data))
        return failures

    def validate_payload(self, data: Any, location: str) -> list[str]:
        failures: list[str] = []
        failures.extend(self._reject_placeholders(data, location))
        failures.extend(self._validate_hashes(data, location))
        failures.extend(self._validate_json_pointers(data, location))
        return failures

    def _reject_placeholders(self, value: Any, location: str) -> list[str]:
        failures: list[str] = []
        if isinstance(value, dict):
            for key, nested in value.items():
                failures.extend(self._reject_placeholders(nested, f"{location}.{key}"))
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                failures.extend(self._reject_placeholders(nested, f"{location}[{index}]"))
        elif isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"example", "todo", "tbd", "placeholder", "not implemented"}:
                failures.append(f"{location}: placeholder value is not semantic evidence")
        return failures

    def _validate_hashes(self, value: Any, location: str) -> list[str]:
        failures: list[str] = []
        if isinstance(value, dict):
            for key, nested in value.items():
                nested_location = f"{location}.{key}"
                if key in {"canonicalHash", "planHash", "bundleHash", "checksum", "sourceHash", "restoredHash"}:
                    if not isinstance(nested, str) or re.fullmatch(r"[0-9a-f]{64}", nested) is None:
                        failures.append(f"{nested_location}: hash must be lowercase 64-character SHA-256")
                failures.extend(self._validate_hashes(nested, nested_location))
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                failures.extend(self._validate_hashes(nested, f"{location}[{index}]"))
        return failures

    def _validate_json_pointers(self, value: Any, location: str) -> list[str]:
        failures: list[str] = []
        if isinstance(value, dict):
            if {"pointer", "tokens", "pointsToMissing", "pointsToNull"}.issubset(value):
                pointer = value["pointer"]
                tokens = value["tokens"]
                if value["pointsToMissing"] and value["pointsToNull"]:
                    failures.append(f"{location}: pointsToMissing and pointsToNull cannot both be true")
                if pointer == "" and tokens != []:
                    failures.append(f"{location}: empty pointer must have no tokens")
                if isinstance(pointer, str) and pointer.startswith("/"):
                    decoded = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
                    if tokens != decoded:
                        failures.append(f"{location}: tokens must equal decoded pointer tokens")
            for key, nested in value.items():
                failures.extend(self._validate_json_pointers(nested, f"{location}.{key}"))
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                failures.extend(self._validate_json_pointers(nested, f"{location}[{index}]"))
        return failures

    def _validate_projection_spec(self, data: dict[str, Any]) -> list[str]:
        dimensions = data.get("dimensions", [])
        return self._validate_dimensions(
            [dimension.get("dimensionID") for dimension in dimensions if isinstance(dimension, dict)],
            "dimensions",
        )

    def _validate_mapping_result(self, data: dict[str, Any]) -> list[str]:
        failures = self._validate_dimensions(
            [binding.get("dimensionID") for binding in data.get("dimensionBindings", [])],
            "dimensionBindings",
        )
        status = data.get("status")
        ambiguities = data.get("ambiguities", [])
        if status == "MAPPED" and ambiguities:
            failures.append("MAPPED result must not contain unresolved ambiguities")
        if status in {"AMBIGUOUS", "BLOCKED", "FAILED"} and not data.get("diagnosticReferences"):
            failures.append(f"{status} mapping requires diagnosticReferences")
        return failures

    def _validate_dimensions(self, dimensions: list[Any], location: str) -> list[str]:
        expected = [f"b{i}" for i in range(9)]
        if dimensions != expected:
            return [f"{location} must contain b0-b8 exactly once in canonical order"]
        return []

    def _validate_diagnostic_chain(self, data: dict[str, Any]) -> list[str]:
        failures: list[str] = []
        diagnostics = data.get("diagnostics", [])
        if not diagnostics:
            return ["DiagnosticChain.diagnostics must be nonempty"]
        if diagnostics[0].get("diagnosticID") != data.get("rootDiagnosticID"):
            failures.append("DiagnosticChain rootDiagnosticID must equal the first diagnostic ID")
        seen: set[str] = set()
        for index, diagnostic in enumerate(diagnostics):
            diagnostic_id = diagnostic.get("diagnosticID")
            parent = diagnostic.get("parentDiagnosticID")
            if diagnostic_id in seen:
                failures.append(f"DiagnosticChain duplicate diagnosticID {diagnostic_id}")
            if index == 0 and parent is not None:
                failures.append("DiagnosticChain root parentDiagnosticID must be null")
            if index > 0 and parent not in seen:
                failures.append(f"DiagnosticChain parent {parent} must reference an earlier diagnostic")
            if not diagnostic.get("ruleReferences"):
                failures.append(f"DiagnosticChain diagnostic {diagnostic_id} must contain ruleReferences")
            seen.add(diagnostic_id)
        return failures

    def _validate_audit_chain(self, data: dict[str, Any]) -> list[str]:
        failures: list[str] = []
        events = data.get("events", [])
        sequences = [event.get("eventSequence") for event in events]
        if sequences != list(range(1, len(events) + 1)):
            failures.append("AuditChain eventSequence values must start at 1 and be contiguous")
        event_ids = [event.get("auditEventID") for event in events]
        if len(event_ids) != len(set(event_ids)):
            failures.append("AuditChain auditEventID values must be unique")
        return failures


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = SemanticInstanceChecker(root).validate()
    return print_result("semantic instance validation", failures, "PASS: schema examples are schema-valid and semantically valid.")


if __name__ == "__main__":
    raise SystemExit(main())
