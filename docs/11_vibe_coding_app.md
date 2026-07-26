# Vibe Coding App

## Tool used
- Tool: Claude (Anthropic), via chat — code generated from a structured prompt (see Prompt log)
- Version / environment, if relevant: Django 4.2/5.x, Python 3, SQLite (Django's default database)

## Selected slice
- Option A / B / C: **Option C — Role-based submission slice**, extended to also implement the audit logging capability (REQ-011/REQ-012) added by the Change Request, since both fit naturally in the same small workflow (answer → evidence → submit → audit trail)
- Why this slice was selected: Option C covers the requirements with the richest, most testable business logic already defined (REQ-002, REQ-003, REQ-004, REQ-005, REQ-008), and including the audit log makes the slice demonstrate the full write-path of the system end-to-end, which is also what Deliverable 12's automated tests will exercise

## Data architecture used
- Persistence option: SQLite (Django's default database, via `migrate`), per REQ-010 / DEC-005
- Main entities/models used: `UserRole`, `Assessment`, `ReadinessQuestion`, `Answer`, `Evidence`, `AuditLog` — all 6 entities from the data architecture, implemented as Django models with migrations `0001_initial.py` and `0002_auditlog.py`
- Link to `docs/10_data_architecture.md`: entities, fields and relationships match the document exactly (Assessment 1—* Answer; ReadinessQuestion 1—* Answer; Answer 1—* Evidence; Assessment 1—* AuditLog; UserRole 1—* AuditLog as actor)

## Requirements implemented

| Requirement | App behaviour |
|---|---|
| REQ-002 | `AnswerForm` (Contributor) saves Yes/No/Partial + optional note against the current assessment (`views.answer_question`) |
| REQ-003 | `EvidenceForm`/`Evidence.clean()` reject saving evidence unless source, owner and freshness_date are all present |
| REQ-004 | `readiness_rules.is_evidence_stale()` flags evidence as stale when freshness_date is more than 90 days old (91+ days) |
| REQ-005 | `readiness_rules.can_submit()` blocks submission unless every critical question has at least one non-stale evidence item |
| REQ-006 | `summary` view lists missing/stale critical items with the specific reason (not answered / no evidence / stale) |
| REQ-008 | `can_submit()` rejects any role other than "Transition Lead" with an explicit authorization error (not silent) |
| REQ-009 | Answering a question with evidence takes 4 discrete interactions (open question → save answer → open evidence form → save evidence), counted at screen/submit level — see note under Manual changes about a measurement ambiguity found here |
| REQ-010 | Persistence is SQLite only, via Django's default `db.sqlite3` |
| REQ-011 | `audit.log_action()` writes one `AuditLog` entry for every Answer/Evidence creation, every Answer update, and every Assessment status change |
| REQ-012 | No view/URL exists to edit or delete an `AuditLog` entry — it is read-only by construction, not just by permission check |

## App flow
1. User selects an acting role from the home page (`RoleSelectForm`) — simulates login without full Django auth.
2. As Contributor: user opens a readiness question, answers Yes/No/Partial (+ optional note), then — once the answer exists — attaches evidence (source, owner, freshness date, reference) on a second screen. Each save creates (or, for a repeated answer, updates) an `AuditLog` entry.
3. As Transition Lead: user reviews the home/summary page (shows missing critical items) and submits. If any critical question lacks fresh evidence, or the role isn't Transition Lead, submission is blocked with a specific error message; otherwise the assessment status becomes "Submitted" and an `AuditLog` entry records the change.

## Validation / business rules implemented

| Rule | Related REQ | Implemented where |
|---|---|---|
| Evidence cannot be saved without source, owner and freshness_date | REQ-003 | `Evidence.clean()` (model, now enforced on every `save()`) + `EvidenceForm.clean_source/clean_owner/clean_freshness_date` (form, double validation) |
| Evidence older than 90 days is stale (exactly 90 = not stale, 91+ = stale) | REQ-004 / DEC-004 | `readiness_rules.is_evidence_stale()` |
| Only Transition Lead can submit; blocked if any critical item is missing/stale | REQ-005, REQ-008 | `readiness_rules.can_submit()`, called from `views.submit_assessment` |
| AuditLog `entity_id` must reference an existing Assessment/Answer/Evidence row (CREATE/UPDATE only, not DELETE) | REQ-011 (implied) / DEC-008, DEC-009 | `audit.validate_entity_reference()`, called from `AuditLog.clean()` on every `save()` |
| Answer updates are logged as "UPDATE" with the previous value, not as a second "CREATE" | REQ-011/AC-1 | `views.answer_question`, tracks `is_update`/`old_response` before saving |

## Prompt log

### Prompt 1
Full structured prompt requesting a small Django prototype for "Option C — Role-based submission slice", specifying: the 6 Django models exactly as defined in `docs/10_data_architecture.md` (including the `AuditLog` polymorphic `entity_type`/`entity_id` reference per DEC-008); the requirement that `entity_id` existence be validated at the application layer since Django/SQLite won't enforce it automatically (DEC-009), except for DELETE actions where the record no longer exists by the time it's logged; the 3 required input fields (question response, evidence metadata, role selector); the 4 validation/business rules (evidence completeness, staleness boundary, submission gate, audit logging); a required summary/audit-trail output view; seed data via a management command; and an explicit instruction to keep the app minimal — no Django auth system, no styling framework, no features beyond what was listed.

### Result
- What was generated: Full Django project (`ams_readiness/` settings + `readiness/` app) with 6 models, 2 migrations, `forms.py` (3 forms), `views.py` (5 views: home, answer_question, add_evidence, submit_assessment, summary), `readiness_rules.py` (pure business-logic functions), `audit.py` (validation + logging helper), a `seed_data` management command, 4 minimal templates, and `admin.py` registering all 6 models.
- What was kept: All of the generated model/rule/view structure — it matched the prompt's data architecture and business rules exactly, including the DELETE-action exception in the audit validation, which the tool handled correctly without needing a follow-up correction.
- What was rejected: Nothing structural was rejected on first generation; four issues were found during manual code review afterwards (see Manual changes) and fixed by hand rather than by re-prompting, since they were small, localized corrections.

## Manual changes

| Change | Reason |
|---|---|
| `answer_question` view now distinguishes CREATE vs UPDATE when logging to AuditLog, setting old_value/new_value accordingly | Generated code always logged "CREATE" even when updating an existing answer, violating REQ-011/AC-1 |
| Added `django.contrib.admin`/`django.contrib.auth` to `INSTALLED_APPS`, `AuthenticationMiddleware`, and the `/admin/` URL route | `admin.py` registered all models but was unreachable — no admin app installed and no URL wired, making the registration dead code |
| Added `full_clean()` override to `Evidence.save()` | Ensures REQ-003 validation always runs even if Evidence is created outside the current view/form (e.g. via admin or shell), matching the pattern already used in `AuditLog.save()` |

## How to run the app

```bash
cd app
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # needed to access /admin/
python manage.py seed_data
python manage.py runserver
```

Then open http://127.0.0.1:8000/ — select a role, answer questions with evidence, attempt to submit, and view the summary/audit trail. Visit http://127.0.0.1:8000/admin/ to browse the underlying data directly.