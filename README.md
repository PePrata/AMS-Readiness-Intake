# AMS Readiness Intake — Requirements Rescue Challenge

## Student
- Name: Pedro Afonso Pinto Prata
- Number: 21807403

## Repository purpose
This repository contains the work developed for the resit exam of Requirements Engineering and Testing.

## Work plan
- Day 1: Repository structure setup; Diagnosis and elicitation started
- Day 2: Diagnosis and elicitation complete; Objectives, CSFs and Requirements complete, Macro Mezzo Micro model complete
- Day 3: Use cases complete; User stories and story split complete; Test Cases, BDD and validation complete; Traceability matrix (incomplete) and explanation
- Day 4: Data architecture rough draft; Traceability matrix baseline; Decision log added; Change request added and changes made (requirements, use cases, user stories, test cases, tracebility matrix, decision log, data architecture rough draft changed); Add data architecture model
- Day 5: Vibe coding simple app complete (Django + SQLite, Option C — role-based submission slice, extended with audit logging)
- Day 6: Automated tests implemented
- Day 7: Requirements quality review

## Use of AI tools
- AI tool(s) used:
- What AI was used for:
- What was manually reviewed/changed:
- Main assumptions introduced:
- Main limitations observed:

## Data architecture
- Persistence option used: SQLite
- Main entities/models: Assessment; UserRole; ReadinessQuestion; Answer; Evidence; AuditLog
- Where the schema/model is defined: docs/10_data_architecture.md (design); app/readiness/models.py and app/readiness/migrations/ (implementation)
- How test data is created: app/readiness/management/commands/seed_data.py (Django management command) - seeds 4 UserRole rows (one per role: Transition Lead, AMS Manager, Contributor, Security Officer) and 5 critical ReadinessQuestion rows (monitoring, DR, access, integrations, SLA)

## Application
- Technology used: Python / Django (SQLite as the default database)
- How to run the app:
  - cd app
  - pip install -r requirements.txt
  - python manage.py migrate
  - python manage.py createsuperuser   # needed to access /admin/
  - python manage.py seed_data
  - python manage.py runserver
- Main implemented feature(s): Role-based submission slice (Option C) — a Contributor can answer readiness questions and attach evidence metadata (source, owner, freshness date, reference); only a Transition Lead can submit the assessment as final, and only when no critical question is missing an answer or missing valid (non-stale) evidence; unauthorized roles are rejected with an explicit error. Extended with an audit trail: every create/update of an Answer, Evidence, or Assessment status change produces a read-only AuditLog entry (actor, role, action type, affected entity, timestamp, old/new value), viewable per assessment.

## Automated tests
- Test framework used:
- How to run the tests:
- Number of tests:
- Current result:

## Test database / test data
- Database or persistence type used:
- How the database/test data is created:
- How to reset the test database:
- Seed/test data file(s):

## Final deliverables
- Diagnosis and elicitation
- Objectives, CSFs and requirements
- Macro/Mezzo/Micro model
- Use cases
- User stories
- Test cases and BDD scenarios
- Traceability matrix
- Decision log
- Change request impact
- Data architecture
- Simple app generated with Vibe Coding
- Automated database-backed tests
- Requirements quality review
- AI usage review
