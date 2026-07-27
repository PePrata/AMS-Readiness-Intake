"""
Shared fixtures for the AMS Readiness Intake automated tests.

Uses Django's test database (created/destroyed automatically by pytest-django
around the whole test session, and rolled back per-test via transactions) —
this is separate from the dev database (db.sqlite3) seeded by
`manage.py seed_data` for manual demoing.

Reproducibility: every test starts from the same known state, built here from
migrations + these fixtures — no manual setup is required to re-run the suite.
"""
import pytest
from datetime import date, timedelta

from readiness.models import UserRole, ReadinessQuestion, Assessment, Answer, Evidence


@pytest.fixture
def users(db):
    """4 UserRole records — one per role (case constraints: Transition Lead,
    AMS Manager, Contributor, Security Officer)."""
    return {
        "lead": UserRole.objects.create(name="Alice Lead", role="Transition Lead"),
        "manager": UserRole.objects.create(name="Bob Manager", role="AMS Manager"),
        "contributor": UserRole.objects.create(name="Carla Contributor", role="Contributor"),
        "security": UserRole.objects.create(name="Dave Security", role="Security Officer"),
    }


@pytest.fixture
def questions(db):
    """5 critical ReadinessQuestion records, matching app/readiness/management/
    commands/seed_data.py."""
    data = [
        ("Is monitoring documented?", "monitoring"),
        ("Is the DR procedure documented?", "DR"),
        ("Is the access procedure documented?", "access"),
        ("Are integration dependencies known?", "integrations"),
        ("Is SLA information available?", "SLA"),
    ]
    return [
        ReadinessQuestion.objects.create(text=t, category=c, is_critical=True)
        for t, c in data
    ]


@pytest.fixture
def assessment(db, users):
    """A single Draft Assessment created by the Transition Lead."""
    return Assessment.objects.create(created_by=users["lead"])


def _answer_with_evidence(assessment, question, actor, freshness_date, response="Yes"):
    """Helper: create an Answer + one Evidence item for a question."""
    answer = Answer.objects.create(assessment=assessment, question=question, response=response)
    evidence = Evidence(
        answer=answer,
        source="Confluence / Ops Wiki",
        owner=actor.name,
        freshness_date=freshness_date,
        reference="https://example.internal/evidence/1",
    )
    evidence.full_clean()
    evidence.save()
    return answer, evidence


@pytest.fixture
def complete_assessment(db, users, questions, assessment):
    """An assessment where all 5 critical questions are answered with fresh
    (today) evidence — the 'complete assessment with valid evidence' test
    data case."""
    for q in questions:
        _answer_with_evidence(assessment, q, users["contributor"], date.today())
    return assessment


@pytest.fixture
def incomplete_assessment(db, users, questions, assessment):
    """An assessment where 4 of 5 critical questions have fresh evidence, and
    one is left completely unanswered — the 'missing critical evidence' test
    data case."""
    for q in questions[:-1]:
        _answer_with_evidence(assessment, q, users["contributor"], date.today())
    # questions[-1] intentionally left unanswered
    return assessment
