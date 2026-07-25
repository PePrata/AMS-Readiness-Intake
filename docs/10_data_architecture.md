ROUGH DRAFT OF ARQUITECTURE:

Assesment * - 1 UserRole (User creates/submits Assesment)
Assesment 1 - * Answer (1 Assesment has multiple Answers to questions)
ReadinessQuestion 1 - * Answer (1 ReadinessQuestion has multiple Answers (from diferent Assesments))
Answer 1 - * Evidence (1 Answer has 1 or more Evidence)
Assessment 1 - * AuditLog (each audit entry is scoped to one Assessment, for querying/filtering)
AuditLog references entity_type + entity_id (Assessment / Answer / Evidence) to record which record was changed
UserRole 1 - * AuditLog (each entry records the acting user)