Feature: System Integrity Check

  Scenario: Agent reports system integrity
    Given the Primordia AI system is active
    When I request an integrity check
    Then the system status should be "operational"
    And the response should contain a timestamp
