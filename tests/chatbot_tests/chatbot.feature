# Created by AndyJ at 04/05/2025

  @chatbot

Feature: Add files to knowledge bank
  Tests related to adding files to knowledge bank

  @add_knowledge_bank_positive
  Scenario: Wellbeing staff should be able to add a file to knowledge bank that has a filename length less than or equal to 20
  Given a wellbeing staff member is logged in

  When the wellbeing staff member adds a new file to the knowledge bank
  And the filename is 15 characters long
  And the filename is not already in use

  Then the file is added to the knowledge bank

  @add_knowledge_bank_positive
  Scenario: Wellbeing staff should be not able to add a file to knowledge bank if filename length is greater than 20
  Given a wellbeing staff member is logged in

  When the wellbeing staff member adds a new file to the knowledge bank
  And the filename is 26 characters long
  And the filename is not already in use

  Then the system will notify the user that filename is too long