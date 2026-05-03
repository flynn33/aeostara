#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import print_result, repo_root_from_arg, validate_schemas_and_examples


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = validate_schemas_and_examples(root)
    return print_result("contract schema validation", failures, "PASS: contract schemas, $ref targets, and examples satisfy base-design gates.")


if __name__ == "__main__":
    raise SystemExit(main())
