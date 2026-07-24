Feature: Intake answers and evidence collection
  The goal is to validate that readiness answers and their evidence metadata are captured correctly, and that only authorized roles can edit them.

  Scenario: Happy path - Contributor adds answer with complete evidence metadata
    Given a Contributor is answering a readiness question
    And provides evidence with source, owner and freshness date
    When the Contributor saves the answer
    Then the answer and evidence are stored against the assessment
    And the evidence is correctly linked to the question

  Scenario: Missing evidence metadata - save is blocked
    Given a Contributor is answering a readiness question
    And the evidence freshness date is left empty
    When the Contributor tries to save the answer
    Then the save is rejected
    And a validation error is displayed for the missing field

  Scenario: Unauthorized user - Security Officer cannot edit intake answers
    Given a Security Officer is viewing a readiness assessment
    When the Security Officer tries to add an intake answer
    Then the action is denied with an authorization error
    And the assessment content remains unchanged
