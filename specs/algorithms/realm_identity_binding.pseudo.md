
# Realm Identity Binding

```text
FUNCTION encode_realm_identity(state) -> RealmIdentity
  IF state is not valid:
    RETURN diagnostic rejection
  encoding = "realm:" + bits_to_binary_string(state.coordinates)
  RETURN RealmIdentity(encoding)
END FUNCTION
```
