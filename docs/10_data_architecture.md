# Data Architecture

## Persistence option
- SQLite / JSON: **SQLite**
- Justification: SQLite offers native relational structure to represent the entities and their relationships (Assessment–Answer–Evidence–AuditLog) and is natively supported by Django. (See DEC-005.)

## Data model overview

| Entity / Model | Purpose | Related requirements |
|----------------|---------|----------------------|
| Assessment | Represents one AMS readiness assessment for a transition; tracks its lifecycle (Draft/Submitted) | REQ-001, REQ-005, REQ-010 |
| Answer | Links a specific readiness question to a specific assessment, storing the response given | REQ-002, REQ-009 |
| Evidence | Stores supporting evidence (source, owner, freshness date) attached to an Answer | REQ-003, REQ-004 |
| ReadinessQuestion | Fixed catalog of critical readiness questions reused across assessments | REQ-002, REQ-006 |
| UserRole | Represents a system user and their role (Transition Lead, AMS Manager, Contributor, Security Officer) | REQ-005, REQ-008 |
| AuditLog | Records every create/update/delete action on Assessment, Answer or Evidence, for auditability | REQ-011, REQ-012 |

## Entity details

### Assessment

| Field        | Type    | Required? | Notes             |
|--------------|---------|-----------|-------------------|
| id           | integer | Yes       | Unique identifier |
| status       | string  | Yes       | "Draft" / "Submitted" |
| created_by   | integer (FK → UserRole) | Yes | Who created the assessment (REQ-001) |
| created_at   | date    | Yes       | Creation date (REQ-001) |
| submitted_by | integer (FK → UserRole) | No | Set only on submission; must be Transition Lead (REQ-005) |
| submitted_at | date    | No        | Set only on submission |

### Answer

| Field         | Type    | Required? | Notes |
|---------------|---------|-----------|---|
| id            | integer | Yes       | Unique identifier |
| assessment_id | integer (FK → Assessment) | Yes | Which assessment this answer belongs to |
| question_id   | integer (FK → ReadinessQuestion) | Yes | Which question is being answered |
| response      | string  | Yes       | "Yes" / "No" / "Partial" (REQ-002) |
| note          | string  | No        | Optional note (REQ-002) |

### Evidence

| Field          | Type    | Required? | Notes |
|----------------|---------|-----------|-------|
| id             | integer | Yes       | Unique identifier |
| answer_id      | integer (FK → Answer) | Yes | Links to the Answer it supports |
| source         | string  | Yes       | Evidence source (REQ-003) |
| owner          | string  | Yes       | Evidence owner (REQ-003) |
| freshness_date | date    | Yes       | Used for the stale evidence rule (REQ-004) |
| reference      | string  | Yes       | Actual evidence content: link/URL, file path, or short description of what was reviewed |

### ReadinessQuestion

| Field       | Type    | Required? | Notes |
|-------------|---------|-----------|-------|
| id          | integer | Yes       | Unique identifier |
| text        | string  | Yes       | e.g. "Is monitoring documented?" |
| category    | string  | Yes       | monitoring / DR / access / integrations / SLA |
| is_critical | boolean | Yes       | Used to decide what counts as "missing critical information" (REQ-004, REQ-006) |

### UserRole

| Field | Type    | Required? | Notes |
|-------|---------|-----------|-------|
| id    | integer | Yes       | Unique identifier |
| name  | string  | Yes       | User's name |
| role  | string  | Yes       | Transition Lead / AMS Manager / Contributor / Security Officer |

### AuditLog

| Field         | Type     | Required? | Notes |
|---------------|----------|-----------|-------|
| id            | integer  | Yes       | Unique identifier |
| assessment_id | integer (FK → Assessment) | Yes | Scopes the entry to one assessment, for filtering (REQ-011) |
| actor_id      | integer (FK → UserRole) | Yes | Who performed the action |
| role          | string   | Yes       | Actor's role at the time of the action |
| action_type   | string   | Yes       | "CREATE" / "UPDATE" / "DELETE" |
| entity_type   | string   | Yes       | "Assessment" / "Answer" / "Evidence" (polymorphic reference, see note below) |
| entity_id     | integer  | Yes       | ID of the affected record |
| field_changed | string   | No        | Only applicable for UPDATE |
| old_value     | string   | No        | Only applicable for UPDATE/DELETE |
| new_value     | string   | No        | Only applicable for CREATE/UPDATE |
| justification | string   | No        | Optional reason, e.g. "outdated evidence" (REQ-011) |
| timestamp     | datetime | Yes       | When the action occurred |

**Note on `entity_type` + `entity_id`:** this is a polymorphic reference, not a standard foreign key — `entity_id` can point to a row in `Answer` or `Evidence` depending on `entity_type`. SQLite/Django do not enforce this automatically, so the application layer validates the reference before saving (see DEC-008 and DEC-009).

## Relationships

| Source entity     | Relationship             | Target entity         |
|-------------------|--------------------------|-----------------------|
| Assessment        | belongs to               | UserRole (created_by) |
| Assessment        | has many                 | Answer                |
| ReadinessQuestion | has many                 | Answer                |
| Answer            | belongs to               | Assessment            |
| Answer            | belongs to               | ReadinessQuestion     |
| Answer            | has many                 | Evidence              |
| Assessment        | has many                 | AuditLog              |
| UserRole          | has many                 | AuditLog (as actor)   |
| AuditLog          | references (polymorphic) | Assessment / Answer / Evidence |

## Validation rules supported

| Rule                                                    | Related REQ | Implemented in app? | Tested by              |
|---------------------------------------------------------|-------------|---------------------|------------------------|
| Evidence source, owner and freshness date are mandatory | REQ-003     | Yes                 | TC-003                 |
| Evidence older than 90 days is flagged as stale         | REQ-004     | Yes                 | TC-005, TC-006         |
| Only Transition Lead can submit an assessment           | REQ-005     | Yes                 | TC-002, TC-004, TC-008 |
| Every action maps to a permitted role                   | REQ-008     | Yes                 | TC-008                 |
| Every create/update/delete on Assessment/Answer/Evidence produces one AuditLog entry | REQ-011 | Yes | TC-010 |
| AuditLog entries cannot be edited or deleted; unrelated events are not logged | REQ-012 | Yes | TC-011 |
| AuditLog `entity_id` must reference an existing record (application-level check) | REQ-011 (implied) | Yes | TBD |