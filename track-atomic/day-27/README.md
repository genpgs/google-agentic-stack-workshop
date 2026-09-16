# DAY 27: Spark Capability Manifest Generator (Python)

**Bug**: Script generates malformed tool declarations missing `type` and `description` fields.

**Explain**:
The Antigravity 2.0 tool declaration schema requires each tool to have a `functionName` and `parameters`. Inside `parameters`, each property must define both a `type` and a `description`. Validation using tools like `jsonschema` ensures that manifests adhere strictly to the API contract. Missing fields will cause runtime schema rejections when the agent attempts to use or register the capabilities.

**Task**:
Fix the generator so that it includes the required `type` and `description` fields for each parameter.

**Instruction**:
Run `bats track-atomic/day-27/test.bats` to check your implementation against the schema validator.
