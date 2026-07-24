# User Stories

## US-001 — Create a readiness assessment

As a Transition Lead,
I want to create a new readiness assessment,
so that I can start collecting transition information for a specific AMS transition.

- Linked requirement(s): REQ-001
- Acceptance Criteria:
  - AC-1: A new assessment can be created with status "Draft".
  - AC-2: The assessment records who created it and when.

## US-002 — Answer readiness questions

As a Contributor,
I want to answer predefined readiness questions,
so that the Transition Lead has the information needed to assess readiness.

- Linked requirement(s): REQ-002
- Acceptance Criteria:
  - AC-1: Can answer each question with Yes/No/Partial and an optional note.
  - AC-2: Answers are saved against the correct assessment.

## US-003 — Attach evidence to an answer

As a Contributor,
I want to attach evidence with source, owner and freshness date to my answers,
so that the information I provide is traceable and verifiable.

- Linked requirement(s): REQ-003
- Acceptance Criteria:
  - AC-1: Cannot save evidence without source, owner and freshness date.
  - AC-2: Can attach more than one piece of evidence to the same answer.

## US-004 — See flagged missing or stale evidence

As an AMS Manager,
I want to see which critical evidence is missing or stale,
so that I know what still needs attention before the transition is considered ready.

- Linked requirement(s): REQ-004
- Acceptance Criteria:
  - AC-1: Evidence older than 90 days is visibly flagged as stale.
  - AC-2: Critical questions with no evidence are listed as missing.

## US-005 — Submit the final assessment

As a Transition Lead,
I want to submit the readiness assessment as final,
so that AMS stakeholders know the transition information is complete and locked.

- Linked requirement(s): REQ-005, REQ-008
- Acceptance Criteria:
  - AC-1: Only a Transition Lead can submit the assessment as final.
  - AC-2: Once submitted the assessment can no longer be edited.

## Story split

### Original story
US-005 — Submit the final assessment

### Split into
- US-005a: As a Transition Lead, I want to be blocked from submitting when critical items are still missing, so that incomplete assessments cannot be finalized by mistake.
- US-005b: As a Transition Lead, I want to submit the assessment once all critical items are resolved, so that the transition is formally marked as ready.

### Justification
The original story contained two different behaviors with separate acceptance criteria: 
1: validating that no critical gaps remain 
2: the actual submission itself. 
Splitting them makes each story independently testable - US-005a can be verified with a negative test (submission blocked), while US-005b can be verified with a happy path test (submission succeeds).
