Feature: Audit trail of readiness assessment changes
  The goal is to validate that changes to readiness assessment information are logged for audit purposes, and that the log is append-only and scoped to assessment data only.

  Scenario: Audit entry recorded when evidence is added
    Given a Contributor is answering a readiness question
    And provides evidence with source, owner and freshness date
    When the Contributor saves the answer
    Then an audit log entry is created recording the actor, role, action, timestamp and new value
    And the entry is linked to the correct assessment

  Scenario: Audit log entries cannot be edited or deleted
    Given an audit log entry already exists for an assessment
    When a user tries to edit or delete that audit log entry
    Then the action is denied
    And the audit log entry remains unchanged

  Scenario: Audit log does not record unrelated system events
    Given a user logs into the system
    When the user only views a readiness assessment without changing any data
    Then no audit log entry is created for that login or view action