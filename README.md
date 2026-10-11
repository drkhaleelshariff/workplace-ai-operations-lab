# Workplace AI Operations Lab

A Windows/Python training project investigating retrieval failures,
evaluation, simulated document permissions, structured logging, and
configuration rollback using fictional workplace policies.

The integrated pipeline returns retrieved passages. It does not yet
generate answers with an LLM.

## Start here

Run `06_integrated_pipeline.ipynb` for the combined request path.
Then run `07_integrated_evaluation.ipynb` and
`08_integrated_rollback.ipynb` for evaluation and recovery exercises.

In each notebook, select **Kernel → Restart Kernel and Run All Cells**.
Run notebooks from the repository root.

## Setup on Windows

Tested environment: Python 3.12.10, JupyterLab 4.6.4, ipykernel 7.4.0.

From Command Prompt:

```bat
git clone https://github.com/drkhaleelshariff/workplace-ai-operations-lab.git
cd workplace-ai-operations-lab
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install jupyterlab==4.6.4 ipykernel==7.4.0
python -m jupyterlab
```

The retrieval module uses Python's standard library.
No API key or GPU is required for the current exercises.

The initial retrieval notebook was verified in a separate virtual
environment in a fresh clone on the same Windows laptop, after
correcting two rerun blockers. Later notebooks were checked through
fresh-kernel execution in the original environment.

## Integrated request path

Configuration validation → query validation → policy validation →
role filtering → permitted document reads → passage ranking →
structured completion log.

`workplace_pipeline.py` implements the shared request function.

| Simulated role | Eligible documents |
| --- | --- |
| employee | Three general workplace policies |
| hr_admin | General policies plus a synthetic restricted HR procedure |

Unknown roles are denied. Roles are caller-supplied inputs, not
authenticated identities.

## What the experiments demonstrate

- Word overlap can miss an answerable paraphrase.
- Query expansion can recover one question while degrading another.
- Related passages may not supply sufficient evidence for an answer.
- Missing documents are operational errors, distinct from no matches.
- Document permissions are applied before content reads and ranking.
- Configuration rollback can restore exact per-case retrieval results.

## Recorded results

Nine development questions include five answerable cases, one of
which requires a qualified answer, and four abstention-reference cases.

| Retrieval measure | Baseline | Experimental expansion |
| --- | --- | --- |
| Supporting passage at rank 1 | 4/5 | 4/5 |
| Supporting passage within top 2 | 4/5 | 5/5 |

The integrated baseline reproduced 4/5 at both ranks.
Expansion remains experimental.

Integrated request-path checks verified ten request/log pairs,
including restricted-content exclusion and explicit failure responses.

Integrated rollback verified nine baseline requests, nine invalid-
configuration requests, and nine recovery requests. All nine recovery
signatures matched baseline; configuration bytes were restored exactly.

These are small development experiments, not general performance
estimates or production reliability measurements.

## Notebooks and documentation

| Notebook | Purpose | Details |
| --- | --- | --- |
| 00_environment_check.ipynb | Verify interpreter and working directory | This README |
| 01_retrieval_baseline.ipynb | Investigate word overlap and expansion | EVALUATION.md |
| 02_evaluation_dataset.ipynb | Create and evaluate development labels | EVALUATION.md |
| 03_observability_and_failures.ipynb | Log requests and test failure handling | OBSERVABILITY.md |
| 04_document_access_control.ipynb | Demonstrate two-role filtering | ACCESS_CONTROL.md |
| 05_incident_and_rollback.ipynb | Simulate an isolated configuration incident | INCIDENT_ROLLBACK.md |
| 06_integrated_pipeline.ipynb | Exercise the shared request module | INTEGRATED_PIPELINE.md |
| 07_integrated_evaluation.ipynb | Evaluate the integrated employee path | INTEGRATED_EVALUATION.md |
| 08_integrated_rollback.ipynb | Verify integrated per-case recovery | INTEGRATED_ROLLBACK.md |

## Evidence and reruns

`data/` contains synthetic documents, access policy, and development labels.
`config/` contains versioned lab configurations.
`evidence/` contains reports, request logs, and environment snapshots.

Reruns create additional evidence files. Save and close notebook tabs
before staging files to avoid committing an earlier output snapshot.

Logs exclude query text and retrieved content. Evaluation reports
include synthetic retrieved passages.

If an existing generated file differs from its expected content,
inspect the difference before replacing or deleting it.

## Current limitations

- No LLM, generated answers, or automatic abstention.
- No authentication or operating-system access enforcement.
- No held-out evaluation, deployed API, or concurrent-request testing.
- No timeouts, retries, centralized monitoring, or log rotation.
- Rollback restores existing retrieval limitations.
- Some validation branches exist but have not been exercised.
- Fingerprints and exact-byte checks may differ after Git line-ending
  conversion; original reports describe the files at measurement time.

This is a training lab, not a production-ready AI service.

## Attribution and license

Code, examples, and documentation were developed with ChatGPT assistance.
The policies and restricted marker are fictional training material.
No client documents or real company policies are included.

No license has been assigned yet.