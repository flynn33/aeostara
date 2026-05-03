
# Surface Difference Generation

Surface differences are evidence only. They do not classify state, choose recovery, or override semantic projection.

```text
FUNCTION generate_surface_differences(observed, desired) -> List[SurfaceDifference]
  differences = []
  WALK desired and observed by JSON Pointer tokens
  FOR each present/missing/replaced/type-changed node:
    append SurfaceDifference with diagnosticReference
  RETURN differences
END FUNCTION
```

A surface difference may trigger semantic projection, but semantic projection determines meaning.
