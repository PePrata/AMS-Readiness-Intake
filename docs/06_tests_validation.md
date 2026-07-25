# Test Cases and Validation

## TC-001 — Create assessment successfully (Happy path)
- Linked REQ/US: REQ-001 / US-001
- Type: System
- Priority: High
- Preconditions: User is logged in as Transition Lead.
- Test data: Valid Transition Lead user account.
- Steps:
  1. Select "Create new assessment".
  2. Confirm creation.
- Expected result: A new assessment is created with status "Draft" creator and creation date recorded.

## TC-002 — Submit assessment with all critical items resolved (Happy path)
- Linked REQ/US: REQ-005 / US-005b
- Type: System
- Priority: High
- Preconditions: Assessment exists with all critical questions answered and evidence attached and fresh.
- Test data: Complete assessment with valid, fresh evidence for all critical questions.
- Steps:
  1. Log in as Transition Lead.
  2. Open the complete assessment.
  3. Select "Submit final assessment".
- Expected result: Assessment status changes to "Submitted"; no missing critical items are reported.

## TC-003 — Save evidence without required fields (Negative)
- Linked REQ/US: REQ-003 / US-003
- Type: Unit
- Priority: High
- Preconditions: Contributor is answering a readiness question.
- Test data: Evidence entry missing the "owner" field.
- Steps:
  1. Answer a readiness question.
  2. Attempt to attach evidence without an owner.
- Expected result: Save is rejected; validation error indicates the owner field is required.

## TC-004 — Submit assessment with missing critical items (Negative)
- Linked REQ/US: REQ-004, REQ-005 / US-005a
- Type: Integration
- Priority: High
- Preconditions: Assessment exists with at least one critical question unanswered or without evidence.
- Test data: Assessment with one critical question missing evidence.
- Steps:
  1. Log in as Transition Lead.
  2. Open the incomplete assessment.
  3. Attempt to submit as final.
- Expected result: Submission is blocked; system displays the missing critical information.

## TC-005 — Evidence at exactly 90 days old (Boundary)
- Linked REQ/US: REQ-004 / US-004
- Type: Unit
- Priority: Medium
- Preconditions: Evidence item exists with freshness date exactly 90 days before today.
- Test data: Evidence with freshness_date = today - 90 days.
- Steps:
  1. Load the assessment containing this evidence.
  2. View the evidence status.
- Expected result: Evidence at exactly 90 days is treated according to the defined rule (not yet flagged as stale).

## TC-006 — Evidence at 91 days old (Boundary)
- Linked REQ/US: REQ-004 / US-004
- Type: Unit
- Priority: Medium
- Preconditions: Evidence item exists with freshness date 91 days before today.
- Test data: Evidence with freshness_date = today - 91 days.
- Steps:
  1. Load the assessment containing this evidence.
  2. View the evidence status.
- Expected result: Evidence is flagged as stale.

## TC-007 — Readiness summary generation time (NFR validation)
- Linked REQ/US: REQ-007
- Type: System
- Priority: Medium
- Preconditions: Assessment exists with 50 readiness questions and evidence items.
- Test data: Assessment populated with 50 questions/evidence entries.
- Steps:
  1. Open the assessment.
  2. Request the readiness summary view.
  3. Measure generation time across 5 runs.
- Expected result: Summary generates in under 3 seconds in at least 4 out of 5 runs.

## TC-008 — Contributor attempts to submit final assessment (Role/security)
- Linked REQ/US: REQ-005, REQ-008 / US-005
- Type: Integration
- Priority: High
- Preconditions: Assessment exists in Draft status.
- Test data: Contributor user account, draft assessment.
- Steps:
  1. Log in as Contributor.
  2. Open the assessment.
  3. Attempt to submit as final.
- Expected result: Action is rejected with an authorization error; assessment remains in "Draft" status.

## TC-009 — Readiness summary lists all missing/stale items and recommendations (Happy path)
- Linked REQ/US: REQ-006
- Type: System
- Priority: Medium
- Preconditions: Assessment has at least one missing critical item and one stale evidence item.
- Test data: Assessment with 1 missing critical question and 1 evidence item older than 90 days.
- Steps:
  1. Log in as Transition Lead.
  2. Open the assessment summary view.
- Expected result: The summary lists the missing item, the stale evidence item, and shows a recommended action for each.

## TC-010 — Audit entry created when evidence is attached (Happy path)
- Linked REQ/US: REQ-011 / US-006
- Type: Integration
- Priority: High
- Preconditions: Contributor is answering a readiness question on an existing draft assessment.
- Test data: Valid evidence (source, owner, freshness date) attached by a Contributor.
- Steps:
  1. Contributor attaches evidence to an answer.
  2. Transition Lead opens the audit trail for the assessment.
- Expected result: A new audit entry exists recording actor=Contributor, action=CREATE, entity=Evidence, timestamp and the new value.

## TC-011 — Audit log entry cannot be edited or deleted (Negative / security)
- Linked REQ/US: REQ-012 / US-006
- Type: Integration
- Priority: High
- Preconditions: At least one audit log entry already exists for an assessment.
- Test data: Existing audit entry from a previous Evidence creation.
- Steps:
  1. Attempt to edit an existing audit log entry directly (UI or API call).
  2. Attempt to delete an existing audit log entry.
- Expected result: Both attempts are rejected; the audit log entry remains unchanged, and no login/page-view or other unrelated event appears in the log.

# Definition of Done

## DoD — Requirement
A requirement is done when:
1. It has a unique ID, clear description, type (functional/non-functional/constraint) and priority.
2. It has at least one measurable acceptance criterion and a validation method.
3. It is linked to at least one objective/CSF and traceable to at least one test case.

## DoD — User Story
A user story is done when:
1. It follows the "As a / I want / so that" format and is linked to at least one requirement.
2. It has at least one acceptance criterion.
3. It has been reviewed against at least one corresponding test case or BDD scenario.

## DoD — Final Delivery
A readiness assessment delivery is done when:
1. All critical readiness questions (monitoring, DR, access, integrations, SLAs) have been answered.
2. Every critical answer has evidence attached with source, owner and a freshness date within the accepted threshold, or is explicitly flagged as missing/stale.
3. The assessment has been formally submitted by a Transition Lead, with no unresolved critical gaps blocking submission.
