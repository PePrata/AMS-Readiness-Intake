Feature: AMS readiness assessment submission
  The goal is to validate that a readiness assessment can only be submitted when critical information is complete, and only by an authorized role.

  Scenario: Happy path - Transition Lead submits complete readiness assessment
    Given a Transition Lead has created a readiness assessment
    And all critical evidence fields are complete
    When the Transition Lead submits the assessment
    Then the assessment is marked as submitted
    And no critical missing information is shown

  Scenario: Missing evidence - submission is blocked
    Given a Transition Lead has created a readiness assessment
    And the DR evidence source is missing
    When the Transition Lead tries to submit the assessment
    Then the submission is blocked
    And the system displays the missing critical information

  Scenario: Unauthorized user - Contributor cannot submit final assessment
    Given a Contributor has edited draft answers
    When the Contributor tries to submit the final assessment
    Then the submission is denied
    And the assessment remains in draft status
