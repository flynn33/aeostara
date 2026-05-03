
# Rule ID Validation

```text
FUNCTION validate_rule_reference(rule) -> Result
  REQUIRE rule.ruleID matches ^ASH-[A-Z]+-[A-Z]+-[0-9]{3}$
  REQUIRE rule.sourceReference points to the ASH baseline or Aeostara binding that consumes it
END FUNCTION
```
