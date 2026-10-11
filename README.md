# Workplace AI Operations Lab

An incremental training lab for investigating workplace AI behavior.
The current milestone examines retrieval using original synthetic policies.
Intended audience: engineers and learners investigating retrieval failures.

## Current status

Implemented:
- Three synthetic workplace policy documents.
- Sentence retrieval using unique word overlap.
- Experimental query expansion.
- Manual evidence review and four additional development checks.
- Timestamped JSON results and an installed-package snapshot.

Not yet implemented:
- LLM answer generation or automatic abstention.
- Authentication, document authorization, or operational monitoring.
- Incident recovery or deployment.

This is a training lab. It is not a production AI service.

## Retrieval flow

Synthetic policy files → sentence passages → token matching →
ranked passages → manual review.

The baseline scores each passage by unique words shared with the question.
The expansion variant adds selected vocabulary mappings before scoring.
Both break score ties using passage IDs.

## Observed results

The baseline missed a PTO paraphrase despite a relevant leave policy.
Query expansion recovered that passage.

On four additional development checks:

| Check | Baseline top result | Expanded top result |
| --- | --- | --- |
| Leave submission | Correct | Incorrect |
| Remote approval | Correct | Correct |
| Lost laptop | Correct | Correct |
| Bonus question | No result, as expected | Irrelevant leave passage |

Baseline matched 4/4 references; expansion matched 2/4.
These counts describe this small development set, not general accuracy.

Decision: retain the original retriever as the baseline and keep
query expansion experimental.

## Important findings

- Related text does not necessarily support an answer.
- A full-time entitlement does not establish contractor entitlement.
- An unspecified reimbursement amount does not mean zero reimbursement.
- Empty retrieval can reflect missing information or a retrieval failure.
- Vocabulary expansion can improve one case while degrading others.
- Retrieval scores are word counts, not confidence probabilities.

## Run locally

Observed environment:
- Windows laptop.
- Python 3.12.10.
- JupyterLab 4.6.4.
- ipykernel 7.4.0.

From Command Prompt in a fresh project copy:

    py -3.12 -m venv .venv
    .venv\Scripts\activate.bat
    python -m pip install jupyterlab==4.6.4 ipykernel==7.4.0
    python -m jupyterlab

Open 01_retrieval_baseline.ipynb.
Select Kernel → Restart Kernel and Run All Cells.
Launch Jupyter from the project root so relative paths resolve correctly.

The existing environment was checked by restarting the kernel and
rerunning the notebook. Installation into a second environment has
not yet been tested.

If a document-content mismatch is reported, inspect the existing file
before changing it. The notebook deliberately avoids overwriting
different source content.

## Files

- 00_environment_check.ipynb: interpreter verification.
- 01_retrieval_baseline.ipynb: data creation and retrieval experiments.
- data/synthetic/: fictional policies.
- evidence/: manual reviews, method comparisons, and package snapshots.

Each run creates new timestamped evidence files.

## Limitations and attribution

The examples and policy text were developed with ChatGPT assistance.
They contain no client documents or real company policy.

Reference judgments are manually specified evaluation labels.
No model-generated answers have been evaluated.
All examined questions are development examples, not a held-out test set.
PTO-to-annual-leave mapping is a lab-specific assumption.

Code and materials have not yet been assigned a license.
