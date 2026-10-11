# Retrieval Logging and Failure Handling

## Run

Open 03_observability_and_failures.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

Each setup-cell execution selects a new JSONL log file under
evidence/logs/. Each completed request appends one JSON event.

## Verified scenarios

| Scenario | Status | Error code |
| --- | --- | --- |
| Answerable leave query | ok | null |
| Cafeteria query with no matches | no_match | null |
| Missing source directory | error | SOURCE_UNAVAILABLE_OR_INVALID |
| top_k=0 | error | INVALID_CONFIGURATION |
| top_k=True | error | INVALID_CONFIGURATION |
| Empty query | error | INVALID_QUERY |

A fresh-kernel run on October 11, 2026 produced six events:
one ok, one no_match, and four errors.

Assertions verified response status, error code, empty failure
results, matching log events, metadata fields, and unique request IDs.

## Log fields

timestamp_utc, request_id, event, status, error_code,
result_count, elapsed_ms.

Query text and retrieved content are excluded from the log.
Retrieved content remains available in successful function responses.

Elapsed time covers validation, document loading, and retrieval.
It excludes the log write.

## Design decisions

- Distinguish valid searches with no matches from source failures.
- Validate top_k as an integer from 1 through 10, excluding booleans.
- Reject blank queries and queries without searchable tokens.
- Handle defined query, configuration, and source errors.
- Let unexpected programming errors and log-write failures propagate.

## Limits

This is an in-process notebook function, not a deployed API service.
Test traffic was deliberately selected; these counts are not
availability or operational error-rate measurements.

Missing-source handling was tested. Permission errors, malformed
documents, log-write failures, timeouts, and concurrent requests
have not been exercised.

No authentication, authorization, retries, log rotation, or
centralized monitoring is implemented.