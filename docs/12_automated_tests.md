# Automated Tests

## Framework used
- PyTest (with `pytest-django`), running against Django's test database (SQLite).

## Test scope
- validation rules (evidence completeness, staleness boundary);
- role rules (submission authorization);
- evidence freshness;
- readiness assessment logic (missing critical items, submission gate);
- database-backed test scenarios (all tests read/write real model instances);
- audit log rules introduced by the Change Request (REQ-011, REQ-012, DEC-008, DEC-009).

## Test database / test data

### Persistence option
- SQLite — Django's test database, created and destroyed automatically by `pytest-django` around the test run (separate from the dev database `app/db.sqlite3` used for manual demoing).

### Database or test data setup
- Schema: created automatically from the existing Django migrations (`0001_initial.py`, `0002_auditlog.py`) — no manual `schema.sql` needed, since the app uses Django ORM/migrations (per the exam's Django-specific allowance).
- Test data: built by `pytest` fixtures in `tests/conftest.py`, not a static seed file — this keeps each test's starting state explicit and reproducible without relying on shared mutable seed rows.
- Reset strategy: `pytest-django`'s `db` fixture wraps every test in a database transaction that is rolled back at the end of the test, so each test starts from a clean, identical state regardless of run order.

### Test data summary

| Data item | Purpose | Related scenario |
|---|---|---|
| 4 `UserRole` fixtures (one per role) | Used across all tests to act as different actors | AT-001–AT-007 |
| 5 critical `ReadinessQuestion` fixtures | Matches the real seed data (monitoring, DR, access, integrations, SLA) | AT-001–AT-003 |
| `complete_assessment` fixture — all 5 questions answered with fresh evidence | Happy path | AT-001, AT-004, AT-004b |
| `incomplete_assessment` fixture — 4 of 5 questions answered, 1 unanswered | Negative test | AT-002 |
| Evidence with `freshness_date` = today − 90 days | Boundary (not yet stale) | AT-003a |
| Evidence with `freshness_date` = today − 91 days | Boundary (stale) | AT-003b |
| Evidence with `freshness_date` = today − 120 days, on an answered question | Stale-evidence-counts-as-missing case | AT-003c |
| Contributor / Security Officer `UserRole` | Role/security tests | AT-004, AT-004b |

This gives well over the minimum 8 records (4 users + 5 questions + assessments/answers/evidence created per test), including both valid and invalid/edge cases, as required.

## Automated tests implemented

| Test ID | Test name | Type | Linked REQ | Uses DB/test data? | Purpose |
|---|---|---|---|---|---|
| AT-001 | `test_AT001_complete_assessment_is_ready_and_submittable` | Happy path | REQ-001, REQ-002, REQ-003, REQ-005 | Yes | Confirms a fully answered, evidenced assessment has no missing items and can be submitted |
| AT-002 | `test_AT002_submission_blocked_when_critical_item_missing` | Negative | REQ-004, REQ-005 | Yes | Confirms an unanswered critical question blocks submission, even for the Transition Lead |
| AT-003a/b | `test_AT003a_evidence_exactly_90_days_old_is_not_stale` / `test_AT003b_evidence_91_days_old_is_stale` | Boundary / validation | REQ-004 / DEC-004 | Yes | Confirms the exclusive 90-day boundary on both edges |
| AT-003c | `test_AT003c_stale_evidence_makes_question_missing` | Boundary / validation | REQ-004 | Yes | Confirms stale evidence is reported as "evidence is stale", distinct from "no evidence" |
| AT-004 | `test_AT004_contributor_cannot_submit_assessment` | Role / security | REQ-005, REQ-008 | Yes | Confirms a Contributor is rejected, even on a complete assessment |
| AT-004b | `test_AT004b_security_officer_cannot_submit_assessment` | Role / security | REQ-005, REQ-008 | Yes | Confirms the rule applies to any non-Transition-Lead role |
| AT-005 | `test_AT005_audit_log_entry_created_when_evidence_is_added` | Happy path (audit) | REQ-011 | Yes | Confirms an AuditLog entry is created with correct fields on Evidence creation |
| AT-006 | `test_AT006_audit_log_rejects_nonexistent_entity_id` | Boundary / validation (audit) | REQ-011 (implied) / DEC-008, DEC-009 | Yes | Confirms the application-level existence check rejects a bad `entity_id` |
| AT-006b | `test_AT006b_audit_log_allows_delete_without_existence_check` | Boundary / validation (audit) | DEC-009 | Yes | Confirms DELETE actions skip the existence check, since the record is already gone |
| AT-007 | `test_AT007_updating_an_answer_logs_update_not_create` | Regression | REQ-011/AC-1 | Yes | Confirms editing an answer produces an UPDATE entry with `old_value` set, not a duplicate CREATE — validates the manual fix from Deliverable 11 |

This exceeds the minimum of 4 tests (1 happy path, 1 negative, 1 boundary, 1 role/security), all linked to requirements and all using the test database.

## How to run tests

```bash
pip install -r tests/requirements-dev.txt
pip install -r app/requirements.txt
cd tests
pytest -v
```

`tests/pytest.ini` points `DJANGO_SETTINGS_MODULE` at `ams_readiness.settings` and adds `../app` (relative to `tests/`) to the Python path, so Django/the `readiness` app can be imported without installing the project as a package. All test-related files (`pytest.ini`, `requirements-dev.txt`, `conftest.py`, `test_readiness_database.py`) live under `tests/`, per the repository structure — only `docs/12_automated_tests.md` and `evidence/test_results.md` sit outside it.

## Test result
test_readiness_database.py::test_AT001_complete_assessment_is_ready_and_submittable PASSED                                  [  9%]
test_readiness_database.py::test_AT002_submission_blocked_when_critical_item_missing PASSED                                 [ 18%]
test_readiness_database.py::test_AT003c_stale_evidence_makes_question_missing PASSED                                        [ 27%]
test_readiness_database.py::test_AT004_contributor_cannot_submit_assessment PASSED                                          [ 36%]
test_readiness_database.py::test_AT004b_security_officer_cannot_submit_assessment PASSED                                    [ 45%]
test_readiness_database.py::test_AT005_audit_log_entry_created_when_evidence_is_added PASSED                                [ 54%]
test_readiness_database.py::test_AT006_audit_log_rejects_nonexistent_entity_id PASSED                                       [ 63%]
test_readiness_database.py::test_AT006b_audit_log_allows_delete_without_existence_check PASSED                              [ 72%]
test_readiness_database.py::test_AT007_updating_an_answer_logs_update_not_create PASSED                                     [ 81%]
test_readiness_database.py::test_AT003a_evidence_exactly_90_days_old_is_not_stale PASSED                                    [ 90%]
test_readiness_database.py::test_AT003b_evidence_91_days_old_is_stale PASSED                                                [100%]

======================================================= 11 passed in 0.93s =======================================================


## Reflection
- What requirement was easiest to test? REQ-004 (staleness rule) — it's a pure date calculation with a clearly defined boundary (DEC-004), so AT-003a/b were straightforward to write and assert.
- What requirement was hardest to test? REQ-009 (usability, "5 or fewer interactions") — this could not be given a meaningful automated test at all, because the acceptance criterion never defines what counts as "one interaction" (screen-level vs. field-level). This ambiguity was only discovered while manually testing the Vibe Coding app (Deliverable 11) and is being resolved in Deliverable 13 (Requirements Quality Review) rather than tested here.
- Did automated tests reveal ambiguity in any requirement? Yes — REQ-009, as above. Also, writing AT-006b clarified that REQ-011 doesn't explicitly say what happens when an audit entry is logged for a DELETE action on a record that (by definition) no longer exists; this was resolved via DEC-009 rather than a requirement change.
- How did the database/test data support the scenarios? Using real Django model instances (not mocks) meant the tests exercise the actual `clean()`/`save()` validation paths (e.g. `Evidence.clean()`, `AuditLog.clean()`), catching the same errors the real app would raise — rather than testing business logic in isolation from persistence.
- What changed after the change request? Tests AT-005, AT-006, AT-006b and AT-007 exist entirely because of the audit logging change request (REQ-011/REQ-012) — none of these would have existed in the original Option C scope.
- What would you improve next? Add Django `test.Client`-based integration tests that go through the actual views (`answer_question`, `add_evidence`, `submit_assessment`) rather than calling `readiness_rules`/`audit` functions directly, to catch view-layer regressions (like the CREATE-vs-UPDATE bug) automatically instead of relying on manual code review.