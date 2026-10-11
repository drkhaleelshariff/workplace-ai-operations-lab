# Integrated Permission-Aware Retrieval Pipeline

## Run

Open 06_integrated_pipeline.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

The notebook imports workplace_pipeline.py and uses
config/integrated/pipeline_v1.json.

## Request path

Configuration validation → query validation → policy validation →
role filtering → permitted document reads → passage ranking →
structured completion log.

Roles are simulated caller inputs, not authenticated identities.
The pipeline returns retrieved passages, not generated answers.

## Verified scenarios

- Employee retrieval of the general leave policy.
- Employee exclusion from restricted HR content.
- HR administrator retrieval of the restricted reference code.
- Unknown-role rejection.
- Empty-query rejection.
- No matches for an absent topic.
- Missing-configuration error.
- No restricted-file read on the employee path.
- Explicit error for a simulated unavailable authorized document.
- Invalid top_k rejection using a temporary configuration.

A fresh-kernel run produced ten request/log pairs:
two ok, three no_match, and five error events.

These are selected test cases, not operational reliability statistics.

## Logging

Logs are written under evidence/integrated_logs/ as JSONL.

Fields:
timestamp_utc, request_id, event, config_version, status,
error_code, result_count, elapsed_ms.

Tests verified matching response/log metadata, expected fields,
nonnegative elapsed time, and unique request IDs.

Logs omit query text, supplied role, document IDs, and retrieved content.
Elapsed time excludes writing the log.

## Access and failure checks

Employee read interception observed only the configuration, access
policy, and three allowed documents. It did not observe a restricted
document content read.

A separate interception raised FileNotFoundError for an allowed
document. The pipeline returned SOURCE_UNAVAILABLE_OR_INVALID.

Temporary invalid configuration files are removed after testing.
The valid configuration and policy documents remain unchanged.

## Limits

No authentication, LLM, answer generation, or automatic abstention.
No shared cache, concurrent-request, or live-service testing.

Unexpected programming errors and log-write failures propagate.
There are no retries, timeouts, log rotation, or deployment controls.

Configuration version is logged, but configuration and module content
fingerprints are not yet recorded in these request logs.

The earlier evaluation and rollback exercises remain separate notebooks;
they have not been integrated into this request function.