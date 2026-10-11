# Simulated Configuration Incident and Rollback

## Run

Open 05_incident_and_rollback.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

Each execution creates a separate folder under evidence/incident_runs/.

## Scenario

The known-good configuration uses top_k=2.
The faulty candidate uses top_k=0, outside the accepted range of 1–10.

The exercise deliberately bypasses pre-activation validation to
demonstrate failure detection and recovery. No deployed service
or real users are involved.

## Procedure and observed results

1. Activate v1 and verify that the leave query retrieves leave_policy:1.
2. Activate the invalid candidate.
3. Detect INVALID_CONFIGURATION through the acceptance check.
4. Restore the known-good configuration in a finally block.
5. Verify retrieval acceptance and byte-for-byte restoration of v1.

On October 11, 2026, the initial exercise and a fresh-kernel rerun
both reported five timeline events and verified recovery.

## Recovery procedure

The notebook retains the known-good configuration bytes before
introducing the fault. It writes those bytes to a temporary file
beside the active file, then replaces the active file using os.replace.

Recovery requires both:
- The leave query retrieves leave_policy:1 first.
- The active configuration bytes exactly match v1.

Restoration is attempted even if an assertion in the fault phase raises.
A filesystem failure can still prevent rollback.

## Evidence

Each incident-run folder contains:
- active_configuration.json: the restored v1 configuration.
- incident_report.json: change record, configuration fingerprints,
  timeline, detected cause, impact, recovery checks, and limitations.

Versioned source configurations remain under config/incident_lab/.

## Proposed prevention

Validate candidates before activation, run acceptance checks before
and after activation, and retain an identified known-good configuration.
These prevention measures are proposed; a deployment gate is not
implemented by this exercise.

## Limits

The acceptance check covers one query, not the full evaluation dataset.
No service restart, concurrent traffic, filesystem failure, or rollback
failure was tested.

The timeline is written after completion rather than persisted live.
No availability or recovery-time objective is established.