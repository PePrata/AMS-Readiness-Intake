# Traceability Matrix

| Objective | CSF    | Requirement | Use Case | User Story | Acceptance Criteria | Test Case / BDD Scenario | Data Entity / Model | Automated Test |
|-----------|--------|-------------|----------|------------|---------------------|--------------------------|---------------------|----------------|
| OBJ-01    | CSF-01 | REQ-001     | UC-001   | US-001     | AC-1, AC-2          | TC-001                   | Assessment, UserRole | AT-TBD         |
| OBJ-01    | CSF-01 | REQ-002     | UC-002   | US-002     | AC-1, AC-2          | Scenario: Happy path (readiness_intake_evidence.feature) | Assessment, Answer, ReadinessQuestion | AT-TBD |
| OBJ-02    | CSF-01 | REQ-003     | UC-002/UC-003 | US-003 | AC-1, AC-2         | TC-003 / Scenario: Missing evidence metadata (readiness_intake_evidence.feature) | Answer, Evidence | AT-TBD |
| OBJ-03    | CSF-03 | REQ-004     | UC-004   | US-004     | AC-1, AC-2          | TC-005, TC-006           | Evidence, Answer | AT-TBD         |
| OBJ-02    | CSF-02 | REQ-005     | UC-005/UC-004 | US-005a, US-005b | AC-1, AC-2 | TC-002, TC-004 / Scenario: Missing evidence — submission is blocked (readiness_submission.feature) | Assessment, UserRole | AT-TBD |
| OBJ-03    | CSF-03 | REQ-006     | UC-006   | —          | AC-1, AC-2          | TC-009                   | Assessment, Answer, Evidence | AT-TBD         |
| OBJ-01    | CSF-01 | REQ-007     | UC-006   | —          | AC-1                | TC-007                   | Assessment, Answer, ReadinessQuestion, Evidence | — (NFR, manual measurement) |
| OBJ-02    | CSF-02 | REQ-008     | UC-005   | US-005a    | AC-1, AC-2          | TC-008 / Scenario: Unauthorized user (readiness_submission.feature) | UserRole | AT-TBD |
| OBJ-01    | CSF-01 | REQ-009     | UC-002   | US-002, US-003 | AC-1            | — (manual review only) | — | — |
| OBJ-01    | CSF-01 | REQ-010     | —        | —          | AC-1                | — (manual review only) | Assessment, Answer, Evidence, UserRole, ReadinessQuestion | — |

## Traceability chain

- Objective: OBJ-02 - Ensure that all information is traceable, current and documented (source, owner & date).
- CSF: CSF-02 - Only authorized roles can create, edit or submit readiness assessments, each operation tracked.
- Requirement: REQ-005 - Restrict final submission to the Transition Lead role.
- Use Case / User Story: UC-005 (Submit final assessment, includes UC-004) / US-005a (blocked when critical items missing), US-005b (submission succeeds when complete).
- Acceptance Criteria: AC-1 (only Transition Lead can submit), AC-2 (attempts by other roles are rejected).
- Test Case / BDD Scenario: TC-004 (negative - missing critical items), TC-008 (role/security - Contributor attempts to submit) / Scenario "Unauthorized user - Contributor cannot submit final assessment" (readiness_submission.feature).
- Automated Test: TBD.
- Explanation:
  - Why the requirement supports the objective: REQ-005 is what enforces CSF-02's demand that only authorized roles submit assessments, which supports OBJ-02's goal of information being controlled and accountable - without this rule, any user could finalize an assessment, undermining traceability of who is responsible for the readiness claim.
  - Why the test validates the requirement: TC-008 and its BDD scenario directly attempt the forbidden action (a Contributor trying to submit) and assert it is rejected, matching REQ-005's AC-2 exactly. TC-004 complements this by validating that submission is also blocked when critical information is missing, linking REQ-005 to REQ-004/CSF-03.
  - What would be affected if the requirement changed: if REQ-005 were relaxed (e.g., AMS Manager also allowed to submit), UC-005, US-005a/b, TC-004, TC-008, the BDD scenario and the future automated test would all need to be updated.
