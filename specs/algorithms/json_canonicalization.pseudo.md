
# JSON Canonicalization

Canonicalization creates stable semantic evidence and hashes. It does not classify state by itself.

```text
FUNCTION canonicalize_json(value) -> bytes
  IF value is object:
    emit "{"
    FOR key IN keys(value) sorted by UTF-8 code unit order:
      emit canonicalize_string(key)
      emit ":"
      emit canonicalize_json(value[key])
      emit comma between entries only
    emit "}"
  ELSE IF value is array:
    emit elements in original array order
  ELSE IF value is string:
    emit canonical JSON string escaping
  ELSE IF value is number:
    emit canonical JSON number representation
  ELSE IF value is true, false, or null:
    emit lowercase JSON literal
END FUNCTION

FUNCTION canonical_hash(value) -> SHA256_HEX
  RETURN sha256(canonicalize_json(value))
END FUNCTION
```
