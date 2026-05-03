
# JSON Pointer Operations

Dot-path addressing is superseded. Aeostara uses JSON Pointer-compatible addressing as the normative model.

## Rules

- The empty pointer addresses the whole document.
- `/` separates tokens.
- `~1` decodes to `/` and `~0` decodes to `~`.
- Object keys containing `.` are ordinary keys and are not split.
- Array tokens are base-10 indexes with no leading-sign syntax.
- Missing is distinct from JSON `null`.

```text
FUNCTION resolve_pointer(document, pointer) -> PointerResolution
  tokens = decode_json_pointer(pointer)
  current = document
  FOR token IN tokens:
    IF current is object:
      IF token is not an own key:
        RETURN {status: MISSING, value: ABSENT, pointsToMissing: true, pointsToNull: false}
      current = current[token]
    ELSE IF current is array:
      IF token is not a valid array index within bounds:
        RETURN {status: MISSING, value: ABSENT, pointsToMissing: true, pointsToNull: false}
      current = current[index(token)]
    ELSE:
      RETURN {status: MISSING, value: ABSENT, pointsToMissing: true, pointsToNull: false}
  END FOR
  RETURN {status: PRESENT, value: current, pointsToMissing: false, pointsToNull: current == null}
END FUNCTION
```

Mutation operations must call `mutation_precondition_check` before modifying a document.
