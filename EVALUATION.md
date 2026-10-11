# Retrieval Evaluation: Development Dataset v1

## Run

Open 02_evaluation_dataset.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

The notebook loads data/evaluation/development_v1.json, validates
referenced passage IDs, compares two retrieval methods, and writes
a timestamped report under evidence/.

## Dataset

Nine manually labeled development questions:
- Four answer cases.
- One qualified-answer case.
- Four abstention cases.

All questions were examined during development. This is not a
held-out test set.

## Metrics

For the five answerable cases, a supporting-passage hit means
at least one reference supporting passage appears within the
specified retrieval ranks.

For the four abstention cases, we separately count cases returning
any passages. This is descriptive, not an abstention accuracy score.

## Observed results

| Measure | Baseline | Query expansion |
| --- | --- | --- |
| Supporting passage at rank 1 | 4/5 | 4/5 |
| Supporting passage within top 2 | 4/5 | 5/5 |
| Abstention cases returning passages | 2/4 | 3/4 |

Expansion recovered the PTO paraphrase but moved the correct
leave-submission passage from first to second place. It also
returned unrelated policy passages for the bonus question.

Retain the baseline and keep expansion experimental.
These results do not establish general retrieval performance.

## Reproduction and evidence

On October 11, 2026, restarting the evaluation notebook kernel
and running all cells reproduced these results in the original
Windows project environment.

Reports include per-case retrieved passages, configuration,
Python/platform details, and SHA-256 fingerprints of the dataset
and three source documents.

Dataset SHA-256:
7163a1f584a7df8806214b263ab7a79e0f25e82ec8ba45e934a04193751d020f

## Limits

Supporting-passage hits do not measure generated-answer correctness.
Diagnostic passages may explain missing evidence without answering
the question. No LLM or automated abstention component was evaluated.