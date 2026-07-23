# Macro / Mezzo / Micro

## Macro

| ID      | Capability                                       | Description                                                                                                                        |
|---------|--------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| MAC-001 | AMS Readiness Assessment                         | Capability to create, fill in and submit a structured readiness assessment for the AMS transition.                                 |
| MAC-002 | Evidence-based Information Governance            | Capability to ensure all readiness information is backed by traceable, current evidence and controlled by role-based access.       |
| MAC-003 | Information Gap Identification & Recommendations | Capability to detect missing or stale critical information and summarize it into actionable recommendations for the first 90 days. |


## Mezzo

| ID      | Functional area                                  | Related Macro |
|---------|--------------------------------------------------|---------------|
| MEZ-001 | Create and manage assessment                     | MAC-001       |
| MEZ-002 | Capture intake answers                           | MAC-001       |
| MEZ-003 | Manage evidence metadata                         | MAC-002       |
| MEZ-004 | Enforce role-based access and submission control | MAC-002       |
| MEZ-005 | Identify missing critical information            | MAC-003       |
| MEZ-006 | Review readiness summary and recommendations     | MAC-003       |


## Micro

| ID      | Rule / Validation                                                                                      | Related Mezzo | Related REQ |
|---------|--------------------------------------------------------------------------------------------------------|---------------|-------------|
| MIC-001 | A new assessment starts with status "Draft"                                                            | MEZ-001       | REQ-001     |
| MIC-002 | Each readiness question is answered Yes/No/Partial with an optional note                               | MEZ-002       | REQ-002     |
| MIC-003 | Evidence source, owner and freshness date are mandatory fields                                         | MEZ-003       | REQ-003     |
| MIC-004 | Evidence older than 90 days must be flagged as stale                                                   | MEZ-005       | REQ-004     |
| MIC-005 | Critical questions without linked evidence are listed as missing                                       | MEZ-005       | REQ-004     |
| MIC-006 | Only Transition Lead can submit the final assessment                                                   | MEZ-004       | REQ-005     |
| MIC-007 | Every action is mapped to at least one permitted role                                                  | MEZ-004       | REQ-008     |
| MIC-008 | The summary must present recommended actions ordered by criticality                                    | MEZ-006       | REQ-006     |
| MIC-009 | Summary calculation completes within 3 seconds for up to 50 questions/evidence items under normal load | MEZ-006       | REQ-007     |
