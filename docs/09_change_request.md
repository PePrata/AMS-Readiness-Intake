# Change Request Impact

## Change request received

New requirement:

Transition Lead: In order to support and document decisions, I need the Readiness Assessment module to have a logging tool to register every and any intervention in the Transition Intake and Readiness Assessment.

This logging tool is not ment to be a tradicional log, where all events are recorded, it's main goal is to permit auditibility of decisson processes and track every piece of information gathered, changed or removed, despicting user, date and, if available, justification (e.g. outdated evidence)

The logging tool must permit full tracking and auditing of any transition acording to normative rules ISO 9001 (Quality Management) and ISO 19011 (Auditing Management Systems). Other ruling may apply, like ISO/IEC 27001 (Information Security), ISO 31000 (Risk Management) and ISO/IEC 38500 (IT Governance)

## Impact analysis

| Artefact | Impact | Updated? |
|---|---|---|
| Requirements | Added REQ-011 and REQ-012 | Yes |
| Use Cases | Added UC-007; updated UC-002 and UC-005 to include audit log entry step. UC-007 primary actor corrected to Transition Lead (matching US-006), with Security Officer as secondary actor, after an inconsistency was found across UC-007/TC-010 | Yes |
| User Stories | Added US-006 | Yes |
| Test Cases | Added TC-010 and TC-011. TC-010 step corrected to have the Transition Lead open the audit trail, aligning with US-006 and the corrected UC-007 | Yes |
| BDD Scenarios | Added `bdd/features/audit_trail.feature` with scenarios "Audit entry recorded when evidence is added", "Audit log entries cannot be edited or deleted" and "Audit log does not record unrelated system events" | Yes |
| Traceability Matrix | Added rows for REQ-011 and REQ-012, linking to UC-007, US-006, TC-010/TC-011 and the AuditLog entity. Also updated REQ-001, REQ-002, REQ-003, REQ-005 and REQ-010 to include AuditLog as a secondary Data Entity, since these requirements involve write actions on Assessment/Answer/Evidence that now also produce an audit entry | Yes |
| Decision Log | Added DEC-007 (audit log scope limited to Assessment/Answer/Evidence, excluding generic events) and DEC-008 (AuditLog uses a polymorphic entity_type/entity_id reference instead of separate per-entity foreign keys) | Yes |
| Data Architecture | Completed the AuditLog definition in `docs/10_data_architecture.md` (it had been left as an unfinished draft): full field list (actor, role, action_type, entity_type, entity_id, field_changed, old_value, new_value, justification, timestamp) and relationships to Assessment and UserRole | Yes |
| Test Database / Test Data | Not yet affected — `app/` and `tests/` have not been implemented; AuditLog entity will be built in from the start instead of being retrofitted later | No |
| Automated Tests | Not yet affected — no automated tests exist yet. Automated Tests will be planned for TC-010/TC-011 when Deliverable 12 is implemented | No |

## Notes on scope decisions

- The client explicitly said this must **not** behave like a generic log ("every event"). REQ-012 and DEC-007 exist specifically to capture that constraint: only changes to readiness-assessment data (Assessment, Answer, Evidence) are logged — not logins, page views or other application events.
- DEC-008 documents a technical trade-off: AuditLog references the changed record via `entity_type` + `entity_id` (a polymorphic reference) rather than three separate nullable foreign keys, one per entity type. This keeps the model simple and extensible, at the cost of not having automatic database-level referential integrity between AuditLog and the referenced Answer/Evidence record — a limitation the application layer must handle explicitly.
