# Diagnosis and Elicitation

## Problems identified

| ID    | Source | Problem                                        | Why it is a problem                                    |
|-------|--------|------------------------------------------------|--------------------------------------------------------|
| P-001 | R1     | "Fast" is not measurable                       | No threshold or context is provided                    |
| P-002 | R2     | "Project data" is too broad                    | No fields, format or scope defined                     |
| P-003 | R3     | "Secure" is not measurable                     | No security controls/metrics listed                    |
| P-004 | R4     | "Dashboard" is a solution, not a need          | The underlying business need is missing                |
| P-005 | R5     | "Use AI" prescribes a technology               | Describes a possible technology not a requirement      |
| P-006 | R6     | "Allow evidence" is unclear                    | Source, owner and freshness date are not defined       |
| P-007 | R7     | "What is missing" is undefined                 | What is 'Critical Information' is not defined          |
| P-008 | R8     | "Microsoft authentication" is a solution       | Describes possible solution not requirement            |
| P-009 | R9     | "Risk scoring" is undefined                    | No model, inputs or thresholds defined                 |
| P-010 | R10    | "User-friendly" is not measurable              | No criteria provided                                   |
| P-011 | Notes  | Stakeholders are inconsistent across sources   | Need to be consistent/defined to assign responsibility |
| P-012 | Notes  | Integrations/dependencies not fully documented | Needed for successful transfer                         |

## Elicitation questions

| ID    | Topic              | Question                                                        | Target stakeholder |
|-------|--------------------|-----------------------------------------------------------------|--------------------|
| Q-001 | Business           | What does "ready for AMS support" mean?                         | Client Manager     |
| Q-002 | Evidence           | What is the missing critical information?                       | Transition Lead    |
| Q-003 | Business           | What are the minimum delivery requirements for next week?       | Client Manager     |
| Q-004 | Security           | What actions can each role perform?                             | Security Officer   |
| Q-005 | AMS Operation      | Who owns each dashboard?                                        | Ops Engineer       |
| Q-006 | Reporting          | What format should the 90-day summary and recommendations have? | Transition Lead    |
| Q-007 | Testing/Validation | What is available to use as test data?                          | Developer          |
| Q-008 | Risk/Continuity    | What risk metrics will be used?                                 | Transition Lead    |
| Q-009 | Evidence           | Who is responsible for registering evidence?                    | Ops Engineer       |
| Q-010 | Evidence           | What happens when evidence is missing/stale?                    | Transition Lead    |
| Q-011 | Security           | Is role based security sufficient?                              | Security Officer   |
| Q-012 | AMS operation      | Which operational areas must be prioritised?                    | Service Owner      |
| Q-013 | Evidence           | What is the threshold for evidence freshness?                   | Transition Lead    |

## Assumptions

| ID    | Assumption                                  | Risk if wrong                              | How to validate                           |
|-------|---------------------------------------------|--------------------------------------------|-------------------------------------------|
| A-001 | Evidence freshness threshold is 90 days     | May require evidence to be more/less fresh | Ask Transition Lead before implementation |
| A-002 | There exist 4 roles: Transition Lead, AMS Manager, Contributor, Security Officer | Extra roles would need role specific permissions | Confirm role list before implementation |
| A-003 | Scope is only Intake & Readiness Assessment | Broader scope would need more requirements | Confirm scope with Client Manager |
| A-004 | Simple database (ex. SQLite) is sufficient (low data volume) | High data volume would require a more complex model | Confirm data volume |
| A-005 | Only Transition Lead can submit the final assessment; Contributor edits drafts only | AMS Manager may also need submission rights | Confirm with Security Officer |
| A-006 | "Missing" means only information from a fixed checklist | Free-text/AI gap detection may be expected | Confirm with Ops Engineer |
