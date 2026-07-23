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

### REQ-001 — Create a readiness assessment
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

### REQ-002 — Add intake answers to readiness questions
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

### REQ-003 — Attach evidence metadata to an answer
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

### REQ-004 — Flag missing or stale critical evidence
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: High
- Description: The system must automatically flag evidence older than 90 days as stale, and flag critical readiness questions with no evidence as missing.
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: Evidence with a freshness date older than 90 days is visually flagged as stale.
  - AC-2: Critical questions without linked evidence are listed as "missing critical information".
- Validation method: Test

### REQ-005 — Restrict final submission to the Transition Lead role
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

### REQ-006 — Provide a summary of missing critical information and recommendations
- Type: Functional
- Stakeholder: Transition Lead, AMS Manager
- Priority: Medium
- Description: The system must generate a summary view listing all missing/stale critical items and a recommended list of actions for the first 90 days.
- Linked objective: OBJ-03
- Linked CSF: CSF-03
- Acceptance Criteria:
  - AC-1: The summary lists every missing or stale critical item found in the assessment.
  - AC-2: The summary is viewable by Transition Lead and AMS Manager roles.
- Validation method: Demo

### REQ-007 — Response time for readiness summary generation
- Type: Non-functional
- Stakeholder: AMS Manager
- Priority: Medium
- Description: The readiness summary view must be generated in under 3 seconds for an assessment with up to 50 readiness questions and evidence items.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Summary generation completes in under 3 seconds measured in at least 4 out of 5 test runs.
- Validation method: Measurement

### REQ-008 — Role-based access control
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

### REQ-009 — Usability of the intake form
- Type: Non-functional
- Stakeholder: Contributor
- Priority: Medium
- Description: A Contributor must be able to complete an intake answer with evidence metadata in at most 5 steps/interactions.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: Completing one readiness answer with evidence requires 5 or fewer user interactions.
  - AC-2: No external documentation required to complete the task.
- Validation method: Review

### REQ-010 — Persistence constraint
- Type: Constraint
- Stakeholder: Developer, Service Owner
- Priority: High
- Description: The system must use only SQLite or JSON-based persistence, as no other is approved for this project.
- Linked objective: OBJ-01
- Linked CSF: CSF-01
- Acceptance Criteria:
  - AC-1: All application data is stored in either a SQLite database or JSON files.
- Validation method: Review
