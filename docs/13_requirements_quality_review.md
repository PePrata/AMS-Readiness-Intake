# Requirements Quality Review

## Review by quality dimension

Legend: ✓ = meets the dimension, ⚠ = partial/borderline, ✗ = fails the dimension.

| REQ     | Clear | Testable | Atomic | Feasible | Traceable | Not impl-specific | Aligned with scope |
|---------|-------|----------|--------|----------|-----------|-------------------|--------------------|
| REQ-001 | ✓     | ✓       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-002 | ✓     | ✓       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-003 | ✓     | ✓       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-004 | ✓     | ✓       | ✗      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-005 | ✓     | ✓       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-006 | ⚠     | ✗       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-007 | ✓     | ✓       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-008 | ⚠     | ⚠       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-009 | ⚠     | ✗       | ✓      | ✓        | ✓        | ✓                 | ✓                  |
| REQ-010 | ✓     | ✓       | ✓      | ✓        | ⚠        | ✓                 | ⚠                  |
| REQ-011 | ✓     | ⚠       | ✓      | ⚠        | ✓        | ✓                 | ✓                  |
| REQ-012 | ✓     | ✓       | ✓      | ✓        | ✓        | ✓                 | ✓                  |

## Quality issues identified

| ID | Requirement | Dimension violated | Description |
|---|---|---|---|
| QI-001 | REQ-009 | Testable | "5 or fewer steps/interactions" never defines what counts as one interaction (a full screen submission vs. each individual field filled). This was only discovered while manually testing the Vibe Coding app (Deliverable 11), where the answer+evidence flow could be measured as 4 interactions (screen-level) or well over 6 (field-level), depending on the reading. |
| QI-002 | REQ-004 | Atomic | The requirement bundles two independent rules in one statement: (a) flagging evidence older than 90 days as stale, and (b) flagging critical questions with no evidence as missing. This was already visible in the Macro/Mezzo/Micro model, where REQ-004 had to be split into two separate Micro rules (MIC-004, MIC-005) — a sign the requirement itself should have been split from the start. |
| QI-003 | REQ-006 | Testable | "a recommended list of actions for the first 90 days" does not define what makes a recommendation valid or complete — there is no rule for how a recommendation is derived from a missing/stale item, so two different implementations could produce entirely different (but equally "compliant") recommendation text, with no way to test which is correct. |
| QI-004 | REQ-010 | Traceable / Aligned with scope | REQ-010 (a technical persistence constraint: SQLite or JSON only) is linked to OBJ-01 ("improve readiness visibility") and CSF-01, but a storage-technology choice has no real conceptual connection to visibility — the link exists only because REQ-010 needed to point to *some* objective, not because one naturally fits. This is an artificial traceability link. |
| QI-005 | REQ-011 | Feasible / Testable | The requirement's rationale references external standards ("audited e.g. against ISO 9001 / ISO 19011") but the requirement itself only specifies structural logging behavior (actor, role, action, timestamp, old/new value). It is feasible to test that this structure exists, but not feasible to test actual "ISO 9001/19011 compliance" from this requirement alone — the ISO reference sets an expectation the requirement cannot fully verify. |
| QI-006 | REQ-008 | Clear | "Every action in the system is mapped to at least one permitted role" (AC-1) does not enumerate what counts as "an action" — is a read (e.g. viewing the summary) an action, or only writes (create/update/delete)? Without this, "every action" cannot be exhaustively checked. |

Six issues identified (minimum required: 4).

## Corrections

### Correction 1 — REQ-009 (resolves QI-001)

**Original:**
 A Contributor must be able to complete an intake answer with evidence metadata in at most 5 steps/interactions.
 - AC-1: Completing one readiness answer with evidence requires 5 or fewer user interactions.

**Corrected:**
 A Contributor must be able to complete one readiness answer, including its evidence metadata, in at most 5 discrete screen submissions.
 - AC-1: Completing one readiness answer with evidence requires 5 or fewer discrete form/screen submissions (each page load that ends in a "Save"/"Submit" action counts as one interaction; filling multiple fields within the same submission does not count as separate interactions).
 - AC-2: No external documentation is required to complete the task.

**Justification:** Defining "interaction" explicitly as "one screen submission" removes the ambiguity that made the requirement untestable in practice. It matches the actual measurement taken during Deliverable 11 testing (4 submissions: open question, save answer, open evidence form, save evidence — which now unambiguously passes), and gives Deliverable 12's automated/manual testers a single, unarguable unit to count.

### Correction 2 — REQ-004 (resolves QI-002)

**Original:**
 REQ-004 - Flag missing or stale critical evidence
 Description: The system must automatically flag evidence older than 90 days as stale, and flag critical readiness questions with no evidence as missing.

**Corrected — split into two atomic requirements:**

**REQ-004a — Flag stale evidence**
 Description: The system must automatically flag evidence with a freshness date more than 90 days old as stale.
 - AC-1: Evidence with a freshness date more than 90 days old is visually flagged as stale.
 - AC-2: Evidence exactly 90 days old or fresher is not flagged as stale.

**REQ-004b — Flag missing critical information**
 Description: The system must flag critical readiness questions that have no answer, or no valid (non-stale) evidence, as missing critical information.
 - AC-1: A critical question with no answer is listed as missing.
 - AC-2: A critical question answered but with no evidence, or only stale evidence, is listed as missing.

**Justification:** These are two independently testable rules with different triggers (an evidence-age check vs. a completeness check across answer+evidence), already implemented as two separate functions in the app (`is_evidence_stale()` and `get_missing_critical_items()`) and tested as separate test cases (TC-005/TC-006 vs. TC-004) and separate Micro rules (MIC-004 vs. MIC-005). Splitting the requirement to match reflects what was already true in every other artefact — the original single REQ-004 was the odd one out.

### Correction 3 — REQ-006 (resolves QI-003)

**Original:**
 Description: The system must generate a summary view listing all missing/stale critical items and a recommended list of actions for the first 90 days.
 - AC-1: The summary lists every missing or stale critical item found in the assessment.

**Corrected:**
 Description: The system must generate a summary view listing all missing/stale critical items, where each item's recommended action is a fixed, deterministic mapping from its reason code (e.g. "not answered" → "Answer this readiness question"; "no evidence" → "Attach supporting evidence"; "evidence is stale" → "Replace evidence with a source no more than 90 days old").
 - AC-1: The summary lists every missing or stale critical item found in the assessment, each with exactly one recommended action drawn from the fixed reason-to-action mapping.
 - AC-2: The summary is viewable by Transition Lead and AMS Manager roles.

**Justification:** Defining recommendations as a fixed, deterministic mapping from reason code to action text makes REQ-006 testable — a test can now assert an exact expected recommendation string for a given missing-item reason, instead of only checking that "some" recommendation text is present. This also removes any risk of the Vibe Coding tool inventing free-text, non-reproducible recommendations in a future regeneration of the app.