"""
readiness_rules.py — Business logic for AMS Readiness Intake.

All rules are implemented here, not inline in templates or views,
so they can be tested independently.
"""

from datetime import date

STALENESS_THRESHOLD_DAYS = 90


def is_evidence_stale(freshness_date: date) -> bool:
    """
    REQ-004 / DEC-004 Staleness rule.

    Evidence is stale when freshness_date is MORE than 90 days old.
    - Exactly 90 days old  → NOT stale  (inclusive lower bound)
    - 91+ days old         → stale       (exclusive upper bound)

    TC-005: freshness_date = today - 90 days  → not stale
    TC-006: freshness_date = today - 91 days  → stale
    """
    delta = date.today() - freshness_date
    return delta.days > STALENESS_THRESHOLD_DAYS


def get_missing_critical_items(assessment) -> list[dict]:
    """
    Return a list of dicts for every critical ReadinessQuestion that is
    NOT fully covered by at least one fresh Evidence item.

    Each dict contains:
        question  — the ReadinessQuestion instance
        reason    — one of: "not answered" | "no evidence" | "evidence is stale"

    Used by the summary view (REQ-004, REQ-006) and the submission gate
    (REQ-005).
    """
    from .models import ReadinessQuestion, Answer

    missing = []
    critical_questions = ReadinessQuestion.objects.filter(is_critical=True)

    for q in critical_questions:
        try:
            answer = Answer.objects.get(assessment=assessment, question=q)
        except Answer.DoesNotExist:
            missing.append({"question": q, "reason": "not answered"})
            continue

        evidence_items = list(answer.evidence_items.all())
        if not evidence_items:
            missing.append({"question": q, "reason": "no evidence"})
            continue

        has_fresh = any(not is_evidence_stale(e.freshness_date) for e in evidence_items)
        if not has_fresh:
            missing.append({"question": q, "reason": "evidence is stale"})

    return missing


def can_submit(assessment, user_role) -> tuple[bool, str | None]:
    """
    REQ-005 / REQ-008 Submission rule.

    Returns (allowed: bool, error_message: str | None).

    Submission is only allowed when:
      1. role == "Transition Lead"
      2. Zero critical ReadinessQuestion rows are unanswered, without
         evidence, or with only stale evidence.

    Any other role → authorization error (not silently ignored).
    """
    if user_role.role != "Transition Lead":
        return (
            False,
            f"Authorization error: role '{user_role.role}' is not permitted to submit. "
            "Only a Transition Lead may submit an assessment.",
        )

    missing = get_missing_critical_items(assessment)
    if missing:
        items = "; ".join(
            f'"{m["question"].text}" ({m["reason"]})' for m in missing
        )
        return (
            False,
            f"Submission blocked: {len(missing)} critical question(s) are not fully "
            f"covered with valid, fresh evidence — {items}.",
        )

    return True, None
