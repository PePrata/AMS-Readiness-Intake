# Use Cases

## Use Case Diagram

![use case](../images/use_case.svg)


## UC-002 — Add intake answers

- Primary actor: Contributor
- Goal: Record answers to critical readiness questions with supporting evidence.
- Preconditions: An assessment exists with status "Draft".
- Trigger: Contributor opens an assessment to fill in or update answers.
- Related requirements: REQ-002, REQ-003

### Main flow
1. Contributor selects a draft assessment.
2. Contributor selects a readiness question.
3. Contributor answers Yes/No/Partial, with an optional note.
4. Contributor attaches evidence with metadata (source, owner, freshness date).
5. System saves the answer and evidence against the assessment.

### Alternative flows
- AF-1: Contributor updates a previously saved answer instead of creating a new one.

### Exceptions
- EX-1: Evidence is submitted without source, owner or freshness date - system rejects the save and shows a validation error.

### Postconditions
- Success: The answer and its evidence are stored and linked to the assessment.
- Failure: No data is saved; the Contributor sees which fields are missing.


## UC-005 — Submit final assessment

- Primary actor: Transition Lead
- Goal: Submit an assessment after confirming no unresolved critical gaps exist.
- Preconditions: An assessment exists with status "Draft"; the actor has the Transition Lead role.
- Trigger: Transition Lead chooses to submit the assessment as final.
- Related requirements: REQ-005, REQ-008

### Main flow
1. Transition Lead opens the assessment.
2. System reviews missing critical information.
3. If no critical items are missing Transition Lead confirms submission.
4. System changes the assessment status to "Submitted".

### Alternative flows
- AF-1: If critical items are missing, the system displays them and returns to editing.

### Exceptions
- EX-1: A user without the Transition Lead role attempts to submit - the system rejects the action and shows an authorization error.

### Postconditions
- Success: Assessment status is "Submitted"; no further edits are allowed.
- Failure: Assessment remains in "Draft" status; the rejection reason is shown.
