
# Codeword Transformation Binding

```text
FUNCTION apply_codeword_transformation(input_state, codeword) -> CodewordTransformation
  REQUIRE codeword is a member of the canonical 16-codeword set
  output.coordinates = xor_each_coordinate(input_state.coordinates, codeword)
  diagnostic = DiagnosticEnvelope(kind=STATE_VALIDITY, ruleReferences=[ASH-CODEWORD-STRUCTURE-001])
  RETURN CodewordTransformation(input_state, codeword, output, diagnostic.ref)
END FUNCTION
```
