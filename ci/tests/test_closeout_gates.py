from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

CI_DIR = Path(__file__).resolve().parents[1]
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))

from semantic_instance_checker import SemanticInstanceChecker
from common_checks import JsonPointerEvaluator
from fixture_validator import FixtureSuiteEvaluator
from workflow_integrity_checker import WorkflowIntegrityChecker


class SemanticInstanceCheckerTests(unittest.TestCase):
    def test_mapping_result_rejects_duplicate_dimensions_and_invalid_pointer_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload_dir = root / "fixtures" / "schema_examples"
            payload_dir.mkdir(parents=True)
            (payload_dir / "MappingResult.example.json").write_text(
                """
                {
                  "mappingResultID": "mapping-result-invalid",
                  "status": "MAPPED",
                  "projectedState": {
                    "stateID": "ash-state-invalid",
                    "coordinates": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "sourceReference": "specs/ash_baseline/ash_state_space_binding.md",
                    "canonicalHash": "0000000000000000000000000000000000000000000000000000000000000000"
                  },
                  "dimensionBindings": [
                    {
                      "dimensionID": "b0",
                      "sourcePointers": [
                        {
                          "pointer": "/system/state",
                          "tokens": [],
                          "pointsToMissing": true,
                          "pointsToNull": true
                        }
                      ],
                      "mappingRule": "map-b0",
                      "evidence": [{"value": 0}],
                      "diagnosticReference": {
                        "diagnosticID": "diagnostic-state-validity-root",
                        "chainRootReference": "diagnostic-state-validity-root",
                        "diagnosticKind": "MAPPING",
                        "ruleReferences": [
                          {
                            "ruleID": "ASH-STATE-VALIDITY-001",
                            "sourceReference": "specs/ash_baseline/state_validity_diagnostic_binding.md",
                            "ruleFamily": "state-validity"
                          }
                        ]
                      }
                    }
                  ],
                  "ambiguities": [],
                  "diagnosticReferences": [
                    {
                      "diagnosticID": "diagnostic-state-validity-root",
                      "chainRootReference": "diagnostic-state-validity-root",
                      "diagnosticKind": "MAPPING",
                      "ruleReferences": [
                        {
                          "ruleID": "ASH-STATE-VALIDITY-001",
                          "sourceReference": "specs/ash_baseline/state_validity_diagnostic_binding.md",
                          "ruleFamily": "state-validity"
                        }
                      ]
                    }
                  ]
                }
                """,
                encoding="utf-8",
            )
            checker = SemanticInstanceChecker(root)
            failures = checker.validate_example(Path("fixtures/schema_examples/MappingResult.example.json"))
        joined = "\n".join(failures)
        self.assertIn("dimensionBindings must contain b0-b8 exactly once", joined)
        self.assertIn("pointsToMissing and pointsToNull cannot both be true", joined)


class JsonPointerEvaluatorTests(unittest.TestCase):
    def test_resolves_dot_key_and_distinguishes_missing_from_null(self) -> None:
        evaluator = JsonPointerEvaluator()
        document = {"feature.flag": True, "items": [None], "nested": {"value": None}}

        dot_key = evaluator.resolve(document, "/feature.flag")
        null_value = evaluator.resolve(document, "/nested/value")
        missing_value = evaluator.resolve(document, "/nested/missing")
        array_value = evaluator.resolve(document, "/items/0")

        self.assertEqual(dot_key.value, True)
        self.assertFalse(dot_key.points_to_missing)
        self.assertFalse(dot_key.points_to_null)
        self.assertFalse(null_value.points_to_missing)
        self.assertTrue(null_value.points_to_null)
        self.assertTrue(missing_value.points_to_missing)
        self.assertFalse(missing_value.points_to_null)
        self.assertFalse(array_value.points_to_missing)
        self.assertTrue(array_value.points_to_null)


class FixtureSuiteEvaluatorTests(unittest.TestCase):
    def test_json_semantics_vector_computes_actual_output(self) -> None:
        evaluator = FixtureSuiteEvaluator(Path.cwd())
        vector = {
            "fixtureID": "json-key-with-dot",
            "category": "object-key-with-dot",
            "sourceReferences": ["specs/algorithms/json_pointer_operations.pseudo.md"],
            "input": {
                "document": {"feature.flag": "enabled"},
                "pointer": "/feature.flag"
            },
            "expected": {
                "diagnosticKind": "STATE_VALIDITY",
                "stateClass": "STABLE",
                "recoveryCategory": "NO_ACTION",
                "mustEmitDiagnostics": True,
                "mustEmitAuditEvents": True,
                "mustMutate": False,
                "resolvedValue": "enabled",
                "pointsToMissing": False,
                "pointsToNull": False,
                "negativeAssertionsExecuted": []
            },
            "negativeAssertions": []
        }
        result = evaluator.evaluate_vector("json_semantics_vectors.json", vector)
        self.assertEqual(result.failures, [])
        self.assertEqual(result.actual["resolvedValue"], "enabled")

    def test_fixture_outputs_reject_placeholder_diagnostics(self) -> None:
        evaluator = FixtureSuiteEvaluator(Path.cwd())
        vector = {
            "fixtureID": "placeholder-output",
            "category": "no-action",
            "sourceReferences": ["specs/algorithms/healing_flow.pseudo.md"],
            "input": {},
            "expected": {
                "diagnosticKind": "STATE_VALIDITY",
                "stateClass": "STABLE",
                "recoveryCategory": "NO_ACTION",
                "mustEmitDiagnostics": True,
                "mustEmitAuditEvents": True,
                "mustMutate": False,
                "requiredSchemaOutputs": [
                    {
                        "schema": "DiagnosticEnvelope.schema.json",
                        "instance": {
                            "diagnosticID": "example",
                            "chainRootReference": "example",
                            "parentDiagnosticID": None,
                            "diagnosticKind": "STATE_VALIDITY",
                            "severity": "INFO",
                            "message": "example",
                            "ruleReferences": [
                                {
                                    "ruleID": "ASH-STATE-VALIDITY-001",
                                    "sourceReference": "example",
                                    "ruleFamily": "example"
                                }
                            ],
                            "sourceReferences": ["example"],
                            "evidence": {}
                        }
                    }
                ],
                "negativeAssertionsExecuted": []
            },
            "negativeAssertions": []
        }
        result = evaluator.evaluate_vector("recovery_escalation_vectors.json", vector)
        self.assertIn("placeholder value is not semantic evidence", "\n".join(result.failures))


class WorkflowIntegrityCheckerTests(unittest.TestCase):
    def test_rejects_failure_suppression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow_dir = root / ".github" / "workflows"
            workflow_dir.mkdir(parents=True)
            (workflow_dir / "weakened.yml").write_text(
                textwrap.dedent(
                    """
                    name: weakened
                    on: [push]
                    jobs:
                      conformance:
                        continue-on-error: true
                        runs-on: ubuntu-latest
                        steps:
                          - run: python3 ci/conformance_runner.py . || true
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            failures = WorkflowIntegrityChecker(root).validate()
        joined = "\n".join(failures)
        self.assertIn("continue-on-error", joined)
        self.assertIn("suppressed failure", joined)


if __name__ == "__main__":
    unittest.main()
