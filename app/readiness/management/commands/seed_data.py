"""
seed_data management command
Usage: python manage.py seed_data

Creates:
  - 4 UserRole rows (one per role)
  - 5 critical ReadinessQuestion rows (categories: monitoring, DR,
    access, integrations, SLA)
  - 1 Assessment owned by the Contributor role

Safe to run multiple times — uses get_or_create so it is idempotent.
"""

from django.core.management.base import BaseCommand
from readiness.models import UserRole, Assessment, ReadinessQuestion


ROLES = [
    {"name": "Alice Transition", "role": "Transition Lead"},
    {"name": "Bob Manager", "role": "AMS Manager"},
    {"name": "Carol Contributor", "role": "Contributor"},
    {"name": "Dave Security", "role": "Security Officer"},
]

QUESTIONS = [
    {
        "text": "Are automated monitoring alerts configured for all production services?",
        "category": "monitoring",
        "is_critical": True,
    },
    {
        "text": "Has a disaster recovery (DR) runbook been tested within the last 6 months?",
        "category": "DR",
        "is_critical": True,
    },
    {
        "text": "Have all privileged access accounts been reviewed and approved?",
        "category": "access",
        "is_critical": True,
    },
    {
        "text": "Are all third-party integrations documented with data-flow diagrams?",
        "category": "integrations",
        "is_critical": True,
    },
    {
        "text": "Have SLA targets been agreed and signed off by all stakeholders?",
        "category": "SLA",
        "is_critical": True,
    },
]


class Command(BaseCommand):
    help = "Seed UserRole and ReadinessQuestion rows for the AMS Readiness prototype."

    def handle(self, *args, **options):
        self.stdout.write("Seeding UserRole rows...")
        roles_created = 0
        for r in ROLES:
            _, created = UserRole.objects.get_or_create(
                role=r["role"], defaults={"name": r["name"]}
            )
            if created:
                roles_created += 1
                self.stdout.write(f"  Created: {r['name']} ({r['role']})")
            else:
                self.stdout.write(f"  Already exists: {r['role']}")

        self.stdout.write("Seeding ReadinessQuestion rows...")
        questions_created = 0
        for q in QUESTIONS:
            _, created = ReadinessQuestion.objects.get_or_create(
                text=q["text"],
                defaults={"category": q["category"], "is_critical": q["is_critical"]},
            )
            if created:
                questions_created += 1
                self.stdout.write(f"  Created [{q['category']}]: {q['text'][:60]}...")
            else:
                self.stdout.write(f"  Already exists [{q['category']}]")

        self.stdout.write("Seeding Assessment...")
        if not Assessment.objects.exists():
            contributor = UserRole.objects.get(role="Contributor")
            Assessment.objects.create(created_by=contributor)
            self.stdout.write("  Created Assessment #1 (Draft, owned by Contributor)")
        else:
            self.stdout.write("  Assessment already exists")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Created {roles_created} role(s) and "
                f"{questions_created} question(s)."
            )
        )
