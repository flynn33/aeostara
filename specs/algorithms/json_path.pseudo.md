# JSON Path Operations (Execution Helper)

Dot-path operations used only by execution helpers and adapters. This module is not a semantic authority.

## get(obj, dotPath) -> value

```text
FUNCTION get(obj, dotPath):
  keys = split(dotPath, ".")
  current = obj
  FOR EACH key IN keys:
    IF current is not object OR key not in current:
      RETURN null
    current = current[key]
  RETURN current
END FUNCTION
```

## set(obj, dotPath, value)

```text
FUNCTION set(obj, dotPath, value):
  keys = split(dotPath, ".")
  current = obj
  FOR i FROM 0 TO length(keys)-2:
    key = keys[i]
    IF key not in current OR current[key] is not object:
      current[key] = {}
    current = current[key]
  current[keys[last]] = value
END FUNCTION
```
