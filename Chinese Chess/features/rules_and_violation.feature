@skip
Feature: Additional Chinese Chess Rules
  As a developer
  I want to test edge cases and special rules in Chinese Chess
  So that I can ensure the game logic is complete and robust

  #################################################################
  # 1) GENERAL - Face-to-face Rule (Black Move)
  #################################################################
  @General
  Scenario: Black moves the General and causes face-to-face (Illegal)
    Given the board has:
      | Piece         | Position |
      | Red General   | (2, 5)   |
      | Black General | (9, 5)   |
    When Black moves the General from (9, 5) to (8, 5)
    Then the move is illegal

  #################################################################
  # 2) CHECK & CHECKMATE
  #################################################################
  @Winning
  Scenario: Red moves to check and Black cannot respond (Red wins)
    Given the board has:
      | Piece         | Position |
      | Red Rook      | (5, 5)   |
      | Black General | (5, 9)   |
    When Red moves the Rook from (5, 5) to (5, 8)
    And Black has no legal move to resolve the check
    Then Red wins by checkmate

  #################################################################
  # 3) ILLEGAL MOVE - Capture own piece
  #################################################################
  @Rule @skip
  Scenario: Red tries to capture its own piece (Illegal)
    Given the board has:
      | Piece         | Position |
      | Red Rook      | (4, 4)   |
      | Red Soldier   | (4, 6)   |
    When Red moves the Rook from (4, 4) to (4, 6)
    Then the move is illegal

  #################################################################
  # 4) ILLEGAL MOVE - Out of board
  #################################################################
  @Rule @skip
  Scenario: Red moves a piece out of board boundaries (Illegal)
    Given the board is empty except for a Red Horse at (1, 1)
    When Red moves the Horse from (1, 1) to (0, 0)
    Then the move is illegal

  #################################################################
  # 5) TURN CONTROL
  #################################################################
  @Turn
  Scenario: Red moves twice in a row (Illegal)
    Given it is Red's turn
    And Red just moved a Rook
    When Red tries to move a Cannon
    Then the move is illegal because it's Black's turn

  #################################################################
  # 6) BLOCKED PATH - Rook blocked by own piece
  #################################################################
  @Rook @skip
  Scenario: Red Rook cannot move because own piece blocks the path
    Given the board has:
      | Piece         | Position |
      | Red Rook      | (4, 1)   |
      | Red Soldier   | (4, 3)   |
    When Red moves the Rook from (4, 1) to (4, 5)
    Then the move is illegal

  #################################################################
  # 7) BLOCKED PATH - Cannon movement blocked by piece
  #################################################################
  @Cannon @skip
  Scenario: Red Cannon cannot move forward because a piece blocks the way
    Given the board has:
      | Piece         | Position |
      | Red Cannon    | (6, 2)   |
      | Red Soldier   | (6, 4)   |
    When Red moves the Cannon from (6, 2) to (6, 8)
    Then the move is illegal

  #################################################################
  # 8) BLOCKED PATH - Horse leg block in other direction
  #################################################################
  @Horse @skip
  Scenario: Red Horse is blocked by leg in another direction
    Given the board has:
      | Piece        | Position |
      | Red Horse    | (5, 5)   |
      | Black Guard  | (5, 6)   |
    When Red moves the Horse from (5, 5) to (6, 7)
    Then the move is illegal

  #################################################################
  # 9) BLOCKED PATH - Elephant eye block in other direction
  #################################################################
  @Elephant @skip
  Scenario: Red Elephant is blocked in southeast direction
    Given the board has:
      | Piece         | Position |
      | Red Elephant  | (3, 5)   |
      | Black Soldier | (4, 6)   |
    When Red moves the Elephant from (3, 5) to (5, 7)
    Then the move is illegal

  #################################################################
  # 10) SOLDIER BLOCKED - cannot move forward when blocked
  #################################################################
  @Soldier @skip
  Scenario: Red Soldier cannot move forward if blocked by own piece
    Given the board has:
      | Piece        | Position |
      | Red Soldier  | (4, 5)   |
      | Red Guard    | (3, 5)   |
    When Red moves the Soldier from (4, 5) to (3, 5)
    Then the move is illegal