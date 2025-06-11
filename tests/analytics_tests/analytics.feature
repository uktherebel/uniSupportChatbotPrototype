# Created by AndyJ at 04/05/2025

  @analytics


Feature: Export data trends as a csv file
  Tests related to exporting data as csv files

  @export_csv_filename_positive
  Scenario: Analytics system should accept a number input when requesting how many themes to export data to a csv file for
  Given a wellbeing officer is logged in

  When the wellbeing officer inputs "8" as the desired number of trends when exporting data to a csv file

  Then a csv file is created with the filename showing there are "8" themes

  @export_csv_filename_negative
  Scenario: Analytics system should not accept a non-number input when requesting how many themes to export data to a csv file for
  Given a wellbeing officer is logged in

  When the wellbeing officer inputs yes as the desired number of trends when exporting data to a csv file

  Then the analytics system will notify the user that they have entered an invalid input