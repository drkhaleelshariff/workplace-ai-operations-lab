# Integrated Configuration Rollback

## Run

Open 08_integrated_rollback.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

Each execution creates an isolated folder under
evidence/integrated_rollback/.

## Exercise

1. Copy the known-good integrated configuration into the run folder.
2. Capture results for all nine development questions as employee.
3. Deliberately activate a candidate with top_k=0.
4. Verify all nine requests return INVALID_CONFIGURATION.
5. Restore the known-good bytes in a finally block.
6. Rerun all nine questions and compare with baseline.

All requests use workplace_pipeline.retrieve_request.

## Recovery criteria

- Active configuration bytes exactly match the known-good configuration.
- All nine per-case signatures match baseline.

Signatures include configuration version, status, error code,
result count, and ordered passage IDs, text, and scores.
They exclude request IDs, timestamps, and elapsed times.

Recovery restores existing baseline behavior, including the PTO
retrieval miss. It does not establish answer correctness.

## Observed evidence

On October 11, 2026, the initial exercise and fresh-kernel rerun
both verified:
- Nine invalid-configuration responses.
- Byte-for-byte configuration restoration.
- Restoration of all nine per-case results.
- Five incident timeline events.
- Twenty-seven matching request/log pairs with unique request IDs.

## Run files

- active_configuration.json: restored configuration.
- invalid_candidate.json: intentionally faulty candidate.
- requests.jsonl: baseline, failure, and recovery completion events.
- rollback_report.json: timeline, comparisons, and fingerprints.

Fingerprints cover the known-good configuration, faulty candidate,
module, dataset, and request log.

## Limits

This is an in-process simulation with caller-supplied roles.
No live users, deployed service, or concurrent traffic were involved.

Development questions are not a held-out test set.
No filesystem failure or rollback failure was injected.
Source documents and policy are not fingerprinted in this report.
The timeline is saved after completion, not persisted live.

Pre-activation validation was deliberately bypassed.
A deployment validation gate is not implemented.