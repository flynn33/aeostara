#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import print_result, repo_root_from_arg, validate_schemas_and_examples


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = validate_schemas_and_examples(root)
    return print_result("schema instance validation", failures, "PASS: schemas, refs, and examples validated.")


if __name__ == "__main__":
    raise SystemExit(main())
