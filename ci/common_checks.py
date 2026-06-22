#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Any

try:
    from jsonschema import Draft7Validator, RefResolver
except ModuleNotFoundError:  # pragma: no cover - exercised in environments without installed requirements.
    Draft7Validator = None  # type: ignore[assignment]
    RefResolver = None  # type: ignore[assignment]

FINAL_JUDGMENTS = {"CONFORMANT", "CONFORMANT WITH CAVEATS", "NON-CONFORMANT"}
REQUIRED_FIXTURE_FILES = [
    "ash_codeword_vectors.json",
    "state_admissibility_vectors.json",
    "semantic_projection_vectors.json",
    "json_semantics_vectors.json",
    "diagnostic_chain_vectors.json",
    "recovery_escalation_vectors.json",
    "policy_block_vectors.json",
    "backup_rollback_vectors.json",
    "safe_halt_terminal_vectors.json",
    "end_to_end_healing_vectors.json",
]
REQUIRED_ASH_BINDINGS = [
    "ash_state_space_binding.md",
    "canonical_codeword_set_binding.md",
    "codeword_transformation_binding.md",
    "state_admissibility_binding.md",
    "state_validity_diagnostic_binding.md",
    "system_state_classification_binding.md",
    "recoverability_binding.md",
    "fallback_policy_registry_binding.md",
    "containment_safe_halt_binding.md",
    "realm_identity_binding.md",
    "transition_registry_binding.md",
    "topology_generator_binding.md",
    "axiom_evaluator_binding.md",
    "generation_materialization_boundary.md",
    "invariant_coverage_map.md",
]
REQUIRED_SCHEMA_NAMES = [
    "AshState.schema.json",
    "CanonicalCodewordSet.schema.json",
    "CodewordTransformation.schema.json",
    "AdmissibilityResult.schema.json",
    "RealmIdentity.schema.json",
    "TransitionDefinition.schema.json",
    "TransitionResult.schema.json",
    "TopologyPlan.schema.json",
    "AxiomDiagnostic.schema.json",
    "GenerationPlan.schema.json",
    "ArtifactEmissionPlan.schema.json",
    "JsonPointer.schema.json",
    "JsonDocumentReference.schema.json",
    "JsonMutationOperation.schema.json",
    "JsonCanonicalizationRule.schema.json",
    "SurfaceDifference.schema.json",
    "SemanticProjectionSpec.schema.json",
    "SemanticDimensionBinding.schema.json",
    "MappingResult.schema.json",
    "MappingAmbiguity.schema.json",
    "DiagnosticEnvelope.schema.json",
    "DiagnosticChain.schema.json",
    "DiagnosticReference.schema.json",
    "RuleReference.schema.json",
    "RecoveryStep.schema.json",
    "RecoveryOutcome.schema.json",
    "EscalationDecision.schema.json",
    "PolicyBundle.schema.json",
    "PolicyDecision.schema.json",
    "BackupRecord.schema.json",
    "BackupResult.schema.json",
    "ExecutionContext.schema.json",
    "ExecutionStepResult.schema.json",
    "RollbackResult.schema.json",
    "VerificationPlan.schema.json",
    "AuditChain.schema.json",
    "HealResult.schema.json",
    "DryRunResult.schema.json",
]


def repo_root_from_arg(argv: list[str], script_file: str) -> Path:
    if len(argv) > 1:
        return Path(argv[1]).resolve()
    return Path(script_file).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class JsonPointerResolution:
    pointer: str
    tokens: tuple[str, ...]
    value: Any
    points_to_missing: bool
    points_to_null: bool


class CanonicalJson:
    def serialize(self, value: Any) -> str:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    def sha256(self, value: Any) -> str:
        return hashlib.sha256(self.serialize(value).encode("utf-8")).hexdigest()


class JsonPointerEvaluator:
    def decode_tokens(self, pointer: str) -> tuple[str, ...]:
        if pointer == "":
            return ()
        if not pointer.startswith("/"):
            raise ValueError(f"JSON Pointer must be empty or start with '/': {pointer}")
        tokens: list[str] = []
        for raw in pointer.split("/")[1:]:
            index = 0
            decoded = ""
            while index < len(raw):
                char = raw[index]
                if char == "~":
                    if index + 1 >= len(raw) or raw[index + 1] not in {"0", "1"}:
                        raise ValueError(f"invalid JSON Pointer escape in {pointer}")
                    decoded += "~" if raw[index + 1] == "0" else "/"
                    index += 2
                    continue
                decoded += char
                index += 1
            tokens.append(decoded)
        return tuple(tokens)

    def resolve(self, document: Any, pointer: str) -> JsonPointerResolution:
        tokens = self.decode_tokens(pointer)
        current = document
        if pointer == "":
            return JsonPointerResolution(pointer, tokens, current, False, current is None)
        for token in tokens:
            if isinstance(current, dict):
                if token not in current:
                    return JsonPointerResolution(pointer, tokens, None, True, False)
                current = current[token]
                continue
            if isinstance(current, list):
                if not token.isdecimal():
                    return JsonPointerResolution(pointer, tokens, None, True, False)
                index = int(token)
                if index >= len(current):
                    return JsonPointerResolution(pointer, tokens, None, True, False)
                current = current[index]
                continue
            return JsonPointerResolution(pointer, tokens, None, True, False)
        return JsonPointerResolution(pointer, tokens, current, False, current is None)


def schema_key(schema_name: str) -> str:
    return schema_name.replace(".schema.json", "")


def load_schemas(root: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    failures: list[str] = []
    schemas: dict[str, dict[str, Any]] = {}
    contracts_dir = root / "specs" / "contracts"
    for path in sorted(contracts_dir.glob("*.schema.json")):
        try:
            data = load_json(path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"invalid JSON schema {path.relative_to(root)}: {exc}")
            continue
        schemas[path.name] = data
        for required in ["$schema", "title", "type"]:
            if required not in data:
                failures.append(f"schema {path.name} missing {required}")
    for name in REQUIRED_SCHEMA_NAMES:
        if name not in schemas:
            failures.append(f"missing required schema: specs/contracts/{name}")
    return schemas, failures


def collect_refs(obj: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(obj, dict):
        ref = obj.get("$ref")
        if isinstance(ref, str):
            refs.append(ref)
        for value in obj.values():
            refs.extend(collect_refs(value))
    elif isinstance(obj, list):
        for value in obj:
            refs.extend(collect_refs(value))
    return refs


def _type_matches(instance: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return (isinstance(instance, int) or isinstance(instance, float)) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    return True


def validate_instance(instance: Any, schema: dict[str, Any], schemas: dict[str, dict[str, Any]], path: str = "$", stack: tuple[str, ...] = ()) -> list[str]:
    failures: list[str] = []
    if "$ref" in schema:
        target = schema["$ref"]
        if target not in schemas:
            return [f"{path}: unresolved $ref {target}"]
        if target in stack:
            return []
        return validate_instance(instance, schemas[target], schemas, path, stack + (target,))
    if not schema:
        return []
    if "const" in schema and instance != schema["const"]:
        failures.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        failures.append(f"{path}: expected one of {schema['enum']!r}, got {instance!r}")
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(_type_matches(instance, item) for item in expected_type):
            failures.append(f"{path}: expected type {expected_type}, got {type(instance).__name__}")
            return failures
        if instance is None:
            return failures
        expected_type = next(item for item in expected_type if item != "null")
    elif isinstance(expected_type, str):
        if not _type_matches(instance, expected_type):
            failures.append(f"{path}: expected type {expected_type}, got {type(instance).__name__}")
            return failures
    if isinstance(instance, str) and "pattern" in schema:
        if re.search(schema["pattern"], instance) is None:
            failures.append(f"{path}: value {instance!r} does not match {schema['pattern']}")
    if expected_type == "array":
        min_items = int(schema.get("minItems", 0))
        max_items = schema.get("maxItems")
        if len(instance) < min_items:
            failures.append(f"{path}: expected at least {min_items} item(s), got {len(instance)}")
        if max_items is not None and len(instance) > int(max_items):
            failures.append(f"{path}: expected at most {max_items} item(s), got {len(instance)}")
        item_schema = schema.get("items", {})
        for index, item in enumerate(instance):
            failures.extend(validate_instance(item, item_schema, schemas, f"{path}[{index}]", stack))
    if expected_type == "object":
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                failures.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    failures.append(f"{path}: unexpected property {key}")
        for key, prop_schema in properties.items():
            if key in instance:
                failures.extend(validate_instance(instance[key], prop_schema, schemas, f"{path}.{key}", stack))
    return failures


def validate_schema_examples(root: Path, schemas: dict[str, dict[str, Any]]) -> list[str]:
    failures: list[str] = []
    examples_dir = root / "fixtures" / "schema_examples"
    for schema_name, schema in schemas.items():
        example_path = examples_dir / f"{schema_key(schema_name)}.example.json"
        if not example_path.is_file():
            failures.append(f"missing example for {schema_name}: {example_path.relative_to(root)}")
            continue
        try:
            instance = load_json(example_path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"invalid example JSON {example_path.relative_to(root)}: {exc}")
            continue
        failures.extend(f"{example_path.relative_to(root)} {issue}" for issue in validate_instance(instance, schema, schemas))
    return failures


def validate_schemas_and_examples(root: Path) -> list[str]:
    schemas, failures = load_schemas(root)
    if Draft7Validator is None or RefResolver is None:
        return failures + ["missing dependency: install ci/requirements.txt for jsonschema Draft 7 validation"]
    for schema_name, schema in schemas.items():
        try:
            Draft7Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"schema {schema_name} is not valid Draft 7: {exc}")
        for target in collect_refs(schema):
            if target not in schemas:
                failures.append(f"schema {schema_name} has unresolved $ref {target}")
    failures.extend(validate_schema_examples_with_jsonschema(root, schemas))
    return failures


def validate_schema_examples_with_jsonschema(root: Path, schemas: dict[str, dict[str, Any]]) -> list[str]:
    failures: list[str] = []
    examples_dir = root / "fixtures" / "schema_examples"
    store = dict(schemas)
    for schema_name, schema in schemas.items():
        example_path = examples_dir / f"{schema_key(schema_name)}.example.json"
        if not example_path.is_file():
            failures.append(f"missing example for {schema_name}: {example_path.relative_to(root)}")
            continue
        try:
            instance = load_json(example_path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"invalid example JSON {example_path.relative_to(root)}: {exc}")
            continue
        resolver = RefResolver.from_schema(schema, store=store)
        validator = Draft7Validator(schema, resolver=resolver)
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
            path = "$" + "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
            failures.append(f"{example_path.relative_to(root)} {path}: {error.message}")
    return failures


def print_result(label: str, failures: list[str], pass_message: str) -> int:
    if failures:
        print(f"FAIL: {label} failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(pass_message)
    return 0
