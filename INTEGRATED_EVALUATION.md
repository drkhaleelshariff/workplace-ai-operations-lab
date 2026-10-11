# Integrated Retrieval Evaluation

## Run

Open 07_integrated_evaluation.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

The notebook evaluates the nine development cases through
workplace_pipeline.retrieve_request using the simulated employee role.

## Passage identifiers

The dataset uses filename-based identifiers.
The integrated module uses document-based identifiers.

| Dataset prefix | Module prefix |
| --- | --- |
| leave_policy | HR-001 |
| remote_work_policy | HR-002 |
| it_support_policy | IT-001 |

Line numbers are preserved. All mapped references are checked against
employee-eligible passages before evaluation.

## Observed results

| Measure | Integrated baseline |
| --- | --- |
| Supporting passage at rank 1 | 4/5 |
| Supporting passage within top 2 | 4/5 |
| Abstention cases returning passages | 2/4 |
| Request statuses | 6 ok, 3 no_match |
| Verified response/log pairs | 9 |

The PTO paraphrase remains a retrieval miss.
No operational errors occurred in these nine selected requests.

Totals match the earlier baseline evaluation. This does not prove
identical rankings, because the passage-ID tie-break order differs.

## Evidence

Each run creates a request log and report under
evidence/integrated_evaluation/.

Reports include per-case responses, support-hit results, ID mappings,
and SHA-256 fingerprints of:
- The Python module.
- The dataset.
- The integrated configuration.
- The access policy.
- Three employee-eligible source documents.

The request log is also fingerprinted. Each response is checked against
exactly one matching log event, with unique request IDs.

A fresh-kernel rerun on October 11, 2026 reached the final report with
nine verified events and seven fingerprinted input/code files.

## Limits

All cases were previously examined during development.
Supporting-passage hits do not measure answer correctness.
Returning passages does not demonstrate correct abstention.

Roles are simulated inputs. No LLM or answer-generation component
was evaluated.

Fingerprints are recorded after evaluation; source and module files
must remain unchanged during the run.