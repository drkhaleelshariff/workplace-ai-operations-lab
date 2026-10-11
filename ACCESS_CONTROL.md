# Two-Role Document Access Demonstration

## Run

Open 04_document_access_control.ipynb from the project root.
Select Kernel → Restart Kernel and Run All Cells.

## Access policy

| Role | Eligible documents | Loaded passages |
| --- | --- | --- |
| employee | Three general policies | 9 |
| hr_admin | General policies plus restricted HR procedure | 11 |

Permissions are defined in data/access_control/policy_v1.json.
Unrecognized roles are denied.

The loader validates document definitions and project-relative paths,
then filters permissions before reading document contents and ranking
passages.

## Verified behavior

A fresh-kernel run on October 11, 2026 confirmed:
- Employee-eligible passages exclude the restricted document and marker.
- Employee retrieval does not return the restricted marker.
- HR administrator retrieval returns the restricted reference code.
- Both roles retrieve the general leave policy.
- An unknown role raises AccessDeniedError.

A separate test intercepted Path.read_text calls during employee
retrieval. It observed four reads: the policy file and three permitted
documents. No restricted-file content read was attempted.

For the tested restricted question, employee retrieval returned zero
results. Other queries may return general passages without revealing
restricted content.

## Evidence

Timestamped access_control_*.json reports under evidence/ contain:
- Policy and restricted-document SHA-256 fingerprints.
- Document IDs read for each role.
- Retrieved results.
- Intercepted employee read paths.

Restricted content and the reference marker are fictional training data.

## Limits

Roles are caller-supplied simulation inputs, not authenticated identities.
A caller able to choose hr_admin can obtain administrator results.

This demonstrates filtering in one application retrieval path.
It does not enforce operating-system permissions or protect the public
synthetic files from direct access.

Shared caches, concurrent requests, policy changes during execution,
and integration with authenticated identities have not been tested.

Malformed-policy and path-validation branches exist but were not
exercised in this milestone. No LLM or answer generation is implemented.