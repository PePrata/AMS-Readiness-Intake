# Objectives, CSFs and Requirements

## Product Objectives

OBJ-01 - Improve readiness visibility for AMS transition stakeholders by centralizing information.

OBJ-02 - Ensure that all information is traceable, current and documented (source, owner & date).

OBJ-03 - Identify information gaps and actionable recommendations for the first 90 days of AMS operation.


## Critical Success Factors

CSF-01 - Critical AMS transition information is complete, current and easily/centrally accessible.

CSF-02 - Only authorized roles can create, edit or submit readiness assessments, each operation tracked.

CSF-03 - Missing or stale critical information is automatically flagged so gaps are visible before the transition is considered complete.


## Structured requirements

### REQ-001 - Create a readiness assessment
- Type: Functional
- Stakeholder: Transition Lead
- Priority: High
- Description: The system must allow a Transition Lead to create a new AMS readiness assessment for a given transition.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: A Transition Lead can start a new assessment with a status of "Draft".
  - AC-2: The assessment records a creation date and creator.
- Validation method: Demo

### REQ-002 - Add intake answers to readiness questions
- Type: Functional
- Stakeholder: Contributor
- Priority: High
- Description: The system must allow a Contributor to answer a predefined set of critical readiness questions (e.g., monitoring documented?, DR procedure documented?).
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Each readiness question can be answered Yes/No/Partial with an optional note.
  - AC-2: Answers are saved against the corresponding assessment.
- Validation method: Test

### REQ-003 - Attach evidence metadata to an answer
- Type: Functional
- Stakeholder: Contributor
- Priority: High
- Description: The system must allow evidence to be linked to a readiness answer, capturing source, owner and freshness date.
- Linked objective: OBJ-02
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Evidence cannot be saved without source, owner and freshness date.
  - AC-2: Multiple evidence items can be linked to the same answer.
- Validation method: Test

### REQ-004a - Flag stale evidence
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: High
- Description: The system must automatically flag evidence with a freshness date more than 90 days old as stale.
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: Evidence with a freshness date more than 90 days old is visually flagged as stale.
  - AC-2: Evidence exactly 90 days old or fresher is not flagged as stale.
- Validation method: Test

### REQ-004b - Flag missing critical information
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: High
- Description: The system must flag critical readiness questions that have no answer, or no valid (non-stale) evidence, as missing critical information.
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: A critical question with no answer is listed as missing.
  - AC-2: A critical question answered but with no evidence, or only stale evidence, is listed as missing.
- Validation method: Test

### REQ-005 - Restrict final submission to the Transition Lead role
- Type: Functional
- Stakeholder: Security Officer
- Priority: High
- Description: The system must ensure that only a user with the Transition Lead role can submit a readiness assessment as final; other roles may only edit drafts.
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: A submit action is only available to users with the Transition Lead role.
  - AC-2: Attempts by other roles to submit are rejected with a clear message.
- Validation method: Test

### REQ-006 - Provide a summary of missing critical information and recommendations
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: Medium
- Description: The system must generate a summary view listing all missing/stale critical items, where each item's recommended action is a fixed mapping from its reason code (e.g. "not answered" → "Answer this readiness question"; "no evidence" → "Attach supporting evidence"; "evidence is stale" → "Replace evidence with a source no more than 90 days old").
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: The summary lists every missing or stale critical item found in the assessment, each with exactly one recommended action drawn from the fixed reason-to-action mapping.
  - AC-2: The summary is viewable by Transition Lead and AMS Manager roles.
- Validation method: Demo

### REQ-007 - Response time for readiness summary generation
- Type: Non-functional
- Stakeholder: AMS Manager
- Priority: Medium
- Description: The readiness summary view must be generated in under 3 seconds for an assessment with up to 50 readiness questions and evidence items.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Summary generation completes in under 3 seconds measured in at least 4 out of 5 test runs.
- Validation method: Measurement

### REQ-008 - Role-based access control
- Type: Non-functional
- Stakeholder: Security Officer
- Priority: High
- Description: The system must enforce role-based access control so that each of the four defined roles (Transition Lead, AMS Manager, Contributor, Security Officer) can only perform the actions permitted for that role.
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: Every action in the system is mapped to at least one permitted role.
  - AC-2: Unauthorized actions return a rejection instead of being silently ignored.
- Validation method: Test

### REQ-009 - Usability of the intake form
- Type: Non-functional
- Stakeholder: Contributor
- Priority: Medium
- Description: A Contributor must be able to complete one readiness answer, including its evidence metadata, in at most 5 discrete screen submissions.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Completing one readiness answer with evidence requires 5 or fewer discrete form/screen submissions (each page load that ends in a "Save"/"Submit" action counts as one interaction; filling multiple fields within the same submission does not count as separate interactions).
  - AC-2: No external documentation is required to complete the task.
- Validation method: Review

### REQ-010 - Persistence constraint
- Type: Constraint
- Stakeholder: Developer, Service Owner
- Priority: High
- Description: The system must use only SQLite or JSON-based persistence, as no other is approved for this project.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: All application data is stored in either a SQLite database or JSON files.
- Validation method: Review

### REQ-011 - Audit log of readiness assessment changes
- Type: Functional
- Stakeholder: Transition Lead, Security Officer
- Priority: High
- Description: The system must record an audit log entry whenever information related to a readiness assessment (Assessment, Answer or Evidence) is created, changed or removed, capturing the actor, role, action type, affected entity/field, timestamp and previous/new value where applicable, so that the decision process can be audited (e.g. against ISO 9001 / ISO 19011 principles).
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: Every create, update or delete action on Assessment, Answer or Evidence produces exactly one audit log entry.
  - AC-2: Each audit log entry records actor, role, action type, entity affected, timestamp and old/new value (for updates).
- Validation method: Test

### REQ-012 - Audit log is append-only and scoped to readiness assessment data
- Type: Non-functional / Constraint
- Stakeholder: Security Officer
- Priority: High
- Description: The audit log must not behave as a generic system log. It must only record entry, change and removal of information about the AMS Readiness Assessment (Assessment, Answer, Evidence) - not unrelated events such as logins or page views - and existing entries must never be editable or deletable through the application.
- Linked objective: OBJ-02
- Linked CSF: CSF-02
- Acceptance Criteria:
  - AC-1: No UI or API action allows editing or deleting an existing audit log entry.
  - AC-2: The audit log contains only entries related to Assessment/Answer/Evidence create/update/delete actions.
- Validation method: Test

## Rewrite of initial poor requirements

| Original                         | Problem                      | Rewritten version                                                  | Justification |
|----------------------------------|------------------------------|--------------------------------------------------------------------------------|---|
| R1: The system must be fast      | Not measurable, no threshold | REQ-007: Readiness summary must generate in under 3 seconds for up to 50 items | Adds testable threshold and defines "fast" |
| R3: The system should be secure  | Not measurable, too broad    | REQ-008: Role-based access control enforced for all 4 roles | Defines "secure" into a testable access-control rule |
| R4: Create a dashboard           | Solution, not a need         | REQ-006: Provide a summary of missing critical information and recommendations | States the business need instead of a solution |
| R6: The app must allow evidence  | Unclear, missing fields      | REQ-003: Attach evidence metadata (source, owner, freshness date) to an answer | Adds the mandatory fields defined in the case constraints making it testable |
| R8: Use Microsoft authentication | Solution not a need          | REQ-005/REQ-008: Restrict submission to Transition Lead role; enforce role-based access control | Replaces specific technology choice with access-control need |
