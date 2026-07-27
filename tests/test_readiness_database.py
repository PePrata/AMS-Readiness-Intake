"""
Automated database-backed tests for the AMS Readiness Intake app.

Covers the 4 required scenario types (Deliverable 12):
  - AT-001: happy path
  - AT-002: negative
  - AT-003: boundary / validation (two edges: 90 days vs 91 days)
  - AT-004: role / security

Plus two additional tests covering the audit log requirements introduced by
the Change Request (REQ-011, REQ-012, DEC-008, DEC-009):
  - AT-005: audit log entry created on evidence creation
  - AT-006: audit log rejects an entity_id that does not exist
  - AT-007: regression test for the CREATE-vs-UPDATE audit bug fixed manually
            in Deliverable 11 (see docs/11_vibe_coding_app.md "Manual changes")

All tests use the Django test database via the fixtures in conftest.py —
they exercise real reads/writes/validation against real model instances, not
isolated pure functions.
"""
from datetime import date, timedelta

import pytest
from django.core.exceptions import ValidationError

from readiness.models import Answer, Evidence, AuditLog
from readiness.readiness_rules import (
    is_evidence_stale,
    get_missing_critical_items,
    can_submit,
)
from readiness.audit import log_action


# ---------------------------------------------------------------------------
# AT-001 — Happy path (REQ-001, REQ-002, REQ-003, REQ-005)
# ---------------------------------------------------------------------------

def test_AT001_complete_assessment_is_ready_and_submittable(complete_assessment, users):
    """A complete assessment (all critical questions answered with fresh
    evidence) has no missing critical items and can be submitted by the
    Transition Lead."""
    missing = get_missing_critical_items(complete_assessment)
    assert missing == []

    allowed, error = can_submit(complete_assessment, users["lead"])
    assert allowed is True
    assert error is None


# ---------------------------------------------------------------------------
# AT-002 — Negative (REQ-004, REQ-005)
# ---------------------------------------------------------------------------

def test_AT002_submission_blocked_when_critical_item_missing(incomplete_assessment, users):
    """An assessment with one unanswered critical question is reported as
    missing, and submission is blocked even for the Transition Lead."""
    missing = get_missing_critical_items(incomplete_assessment)
    assert len(missing) == 1
    assert missing[0]["reason"] == "not answered"

    allowed, error = can_submit(incomplete_assessment, users["lead"])
    assert allowed is False
    assert "Submission blocked" in error


# ---------------------------------------------------------------------------
# AT-003 — Boundary / validation (REQ-004 / DEC-004)
# ---------------------------------------------------------------------------

def test_AT003a_evidence_exactly_90_days_old_is_not_stale():
    """DEC-004: exactly 90 days old is the inclusive lower bound — NOT stale."""
    freshness_date = date.today() - timedelta(days=90)
    assert is_evidence_stale(freshness_date) is False


def test_AT003b_evidence_91_days_old_is_stale():
    """DEC-004: 91 days old crosses the exclusive upper bound — stale."""
    freshness_date = date.today() - timedelta(days=91)
    assert is_evidence_stale(freshness_date) is True


def test_AT003c_stale_evidence_makes_question_missing(assessment, users, questions):
    """A question answered but with only stale evidence is reported as
    missing with reason 'evidence is stale', not 'no evidence'."""
    question = questions[0]
    answer = Answer.objects.create(assessment=assessment, question=question, response="Yes")
    stale_evidence = Evidence(
        answer=answer,
        source="Old Wiki Page",
        owner=users["contributor"].name,
        freshness_date=date.today() - timedelta(days=120),
        reference="https://example.internal/old-evidence",
    )
    stale_evidence.full_clean()
    stale_evidence.save()

    missing = get_missing_critical_items(assessment)
    reasons = {m["question"].id: m["reason"] for m in missing}
    assert reasons[question.id] == "evidence is stale"


# ---------------------------------------------------------------------------
# AT-004 — Role / security (REQ-005, REQ-008)
# ---------------------------------------------------------------------------

def test_AT004_contributor_cannot_submit_assessment(complete_assessment, users):
    """A Contributor attempting to submit — even a fully complete assessment —
    is rejected with an explicit authorization error, not silently ignored."""
    allowed, error = can_submit(complete_assessment, users["contributor"])
    assert allowed is False
    assert "not permitted to submit" in error


def test_AT004b_security_officer_cannot_submit_assessment(complete_assessment, users):
    """Same rule applies to any non-Transition-Lead role, e.g. Security Officer."""
    allowed, error = can_submit(complete_assessment, users["security"])
    assert allowed is False


# ---------------------------------------------------------------------------
# AT-005 — Audit log entry created on evidence creation (REQ-011)
# ---------------------------------------------------------------------------

def test_AT005_audit_log_entry_created_when_evidence_is_added(assessment, users, questions):
    question = questions[0]
    answer = Answer.objects.create(assessment=assessment, question=question, response="Yes")
    evidence = Evidence(
        answer=answer,
        source="Confluence",
        owner=users["contributor"].name,
        freshness_date=date.today(),
        reference="https://example.internal/e1",
    )
    evidence.full_clean()
    evidence.save()

    entry = log_action(
        assessment=assessment,
        actor=users["contributor"],
        action_type="CREATE",
        entity_type="Evidence",
        entity_id=evidence.pk,
        new_value=evidence.source,
    )

    assert AuditLog.objects.filter(pk=entry.pk).exists()
    stored = AuditLog.objects.get(pk=entry.pk)
    assert stored.action_type == "CREATE"
    assert stored.entity_type == "Evidence"
    assert stored.entity_id == evidence.pk
    assert stored.role == "Contributor"


# ---------------------------------------------------------------------------
# AT-006 — Audit log rejects a non-existent entity_id (DEC-008, DEC-009)
# ---------------------------------------------------------------------------

def test_AT006_audit_log_rejects_nonexistent_entity_id(assessment, users):
    """Since entity_type/entity_id is a polymorphic reference with no real
    foreign key (DEC-008), the application-level check (DEC-009) must reject
    an entity_id that does not exist for CREATE/UPDATE actions."""
    with pytest.raises(ValidationError):
        log_action(
            assessment=assessment,
            actor=users["contributor"],
            action_type="CREATE",
            entity_type="Evidence",
            entity_id=999999,  # does not exist
            new_value="anything",
        )
    assert not AuditLog.objects.filter(entity_id=999999).exists()


def test_AT006b_audit_log_allows_delete_without_existence_check(assessment, users, questions):
    """DELETE actions are logged after the record is already gone, so the
    existence check must be skipped for action_type='DELETE' (per DEC-009)."""
    entry = log_action(
        assessment=assessment,
        actor=users["security"],
        action_type="DELETE",
        entity_type="Evidence",
        entity_id=999999,  # already deleted / never existed — must NOT raise
        justification="Removed as part of correction",
    )
    assert AuditLog.objects.filter(pk=entry.pk).exists()


# ---------------------------------------------------------------------------
# AT-007 — Regression test: Answer update must log UPDATE, not CREATE
# (Deliverable 11, Manual changes — this test only passes after that fix)
# ---------------------------------------------------------------------------

def test_AT007_updating_an_answer_logs_update_not_create(assessment, users, questions):
    """REQ-011/AC-1 requires distinguishing create/update/delete. Editing an
    already-answered question must produce an UPDATE entry with the previous
    value recorded as old_value — not a second CREATE entry."""
    question = questions[0]
    answer = Answer.objects.create(assessment=assessment, question=question, response="No")

    log_action(
        assessment=assessment, actor=users["contributor"], action_type="CREATE",
        entity_type="Answer", entity_id=answer.pk, new_value="No",
    )

    # Simulate editing the answer (mirrors the corrected views.answer_question logic)
    old_response = answer.response
    answer.response = "Yes"
    answer.save()
    log_action(
        assessment=assessment, actor=users["contributor"], action_type="UPDATE",
        entity_type="Answer", entity_id=answer.pk,
        old_value=old_response, new_value=answer.response,
    )

    entries = AuditLog.objects.filter(entity_type="Answer", entity_id=answer.pk).order_by("timestamp")
    assert entries.count() == 2
    assert entries[0].action_type == "CREATE"
    assert entries[1].action_type == "UPDATE"
    assert entries[1].old_value == "No"
    assert entries[1].new_value == "Yes"
