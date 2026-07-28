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
- Day 7: Requirements quality review; AI usage review; Final project review

## Use of AI tools
- AI tool(s) used: Claude (Anthropic), via chat
- What AI was used for: Drafting and iterating Deliverables 1–10 and 13 (diagnosis and elicitation, objectives/CSFs/requirements, Macro/Mezzo/Micro model, use cases, user stories, test cases/BDD, traceability matrix, decision log, change request impact, data architecture, requirements quality review); generating the Deliverable 11 Vibe Coding app (Django models, migrations, forms, views, business-logic and audit modules, seed command, templates) from a structured prompt tied to the data architecture; generating the Deliverable 12 automated test suite (pytest-django fixtures and tests) and helping troubleshoot the local pytest/Django setup
- What was manually reviewed/changed: Every AI-drafted document was reviewed before committing, with me drafting first and revising wording/justifications based on AI feedback. The entire generated Django codebase was reviewed; four issues were found and fixed by hand the audit log always recording "CREATE" instead of "UPDATE" on answer edits, the Django admin site being registered but unreachable (missing app/middleware/URL), and evidence validation not running outside the normal form path (missing full_clean() override). The full test suite was also run locally (pytest -v) to confirm all tests actually passed, since the AI tool could not execute them itself. See docs/14_ai_usage_review.md for the full breakdown.
- Main assumptions introduced: That a structured, artifact-referencing prompt (pinned to the existing data architecture, requirements and decision log) would keep AI-generated output aligned with the rest of the documentation rather than letting the tool invent its own design; that AI-generated code and tests still required full manual review and local execution before being treated as correct.
- Main limitations observed: The AI tool could not run Django or pytest in its own environment so the automated tests correctness depended entirely on local execution by me.

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
- Test framework used: PyTest (with pytest-django), running against Django's test database (SQLite)
- How to run the tests:
  - pip install -r tests/requirements-dev.txt
  - pip install -r app/requirements.txt
  - cd tests
  - pytest -v
- Number of tests: 11
- Current result: 11 passed

## Test database / test data
- Database or persistence type used: SQLite
- How the database/test data is created: Schema created automatically from the existing Django migrations
- How to reset the test database: Automatic
- Seed/test data file(s): tests/conftest.py (fixtures); app/readiness/management/commands/seed_data.py (separate seed command used for the manual dev/demo database, not the automated tests)

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
