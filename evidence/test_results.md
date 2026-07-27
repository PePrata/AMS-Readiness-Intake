# Test Results Evidence

## Date/time
2026-07-27 22:40

## Command executed
```
cd tests
pytest -v
```

## Database/test data used
- Persistence option: SQLite (Django test database, auto-created/destroyed by pytest-django)
- Seed file or test data file: N/A — test data is built by `pytest` fixtures in `tests/conftest.py` (4 UserRole + 5 ReadinessQuestion + per-test Assessment/Answer/Evidence), not a static seed file
- Number of records used: 9 baseline fixture records (4 users + 5 questions) plus additional Assessment/Answer/Evidence/AuditLog rows created per test
- Reset strategy before tests: automatic — each test runs inside a database transaction that pytest-django rolls back afterward, so no manual reset step is needed between runs

## Result summary
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


## Notes
- Tests passed: 11
- Tests failed: 0
- Known limitations: These tests exercise `readiness_rules.py` and `audit.py` directly against real model instances (database-backed), not through Django's `test.Client`/views — so a bug purely in view-layer wiring (like the CREATE-vs-UPDATE issue found manually in Deliverable 11) would not necessarily be caught unless mirrored in a test (see AT-007, which specifically encodes the corrected behavior). Full view-level integration tests are noted as a future improvement in docs/12_automated_tests.md.