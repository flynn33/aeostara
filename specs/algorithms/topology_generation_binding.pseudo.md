
# Topology Generation Binding

```text
FUNCTION generate_topology_plan(root_state, depth, transition_registry) -> TopologyPlan
  REQUIRE root_state valid
  nodes and edges are produced in deterministic lexical transition order
  every rejected expansion emits a diagnostic
  RETURN TopologyPlan(nodes, edges, lineage, diagnostics)
END FUNCTION
```
