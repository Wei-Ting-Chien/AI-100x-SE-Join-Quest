@double11_discount
Feature: Double 11 Promotion

  As a customer
  I want to get a discount when buying 10 or more of the same item
  So that I can save money during the Double 11 event

  Scenario: Buy 12 identical items
    Given the Double 11 promotion is active
    And a customer orders the following items:
      | product  | quantity | unitPrice |
      | Socks    | 12       | 100       |
    When the order is submitted
    Then the total price should be 1000

  Scenario: Buy 27 identical items
    Given the Double 11 promotion is active
    And a customer orders the following items:
      | product  | quantity | unitPrice |
      | Socks    | 27       | 100       |
    When the order is submitted
    Then the total price should be 2300

  Scenario: Buy 10 different items
    Given the Double 11 promotion is active
    And a customer orders the following items:
      | product | quantity | unitPrice |
      | A       | 1        | 100       |
      | B       | 1        | 100       |
      | C       | 1        | 100       |
      | D       | 1        | 100       |
      | E       | 1        | 100       |
      | F       | 1        | 100       |
      | G       | 1        | 100       |
      | H       | 1        | 100       |
      | I       | 1        | 100       |
      | J       | 1        | 100       |
    When the order is submitted
    Then the total price should be 1000
