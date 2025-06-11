# Created by AndyJ at 03/05/2025

@appointment_booking


Feature: Book appointments
  Tests related to booking appointments

  @select_appointment_positive
  Scenario: Booking system should accept a number input associated with an available appointment
  Given a student is logged in
  And there is atleast one appointment available

  When the student inputs "1" to indicate that they want appointment one in the booking system

  Then the booking system will add appointment "1" to the student's booking history

  @select_appointment_negative
  Scenario: Booking system should not accept a number input that is not associated with an available appointment
  Given a student is logged in
  And there are only three appointments available

  When the student inputs "4" to indicate that they want appointment four which is not available in the booking system

  Then the booking system will notify user "4" is not associated with an available appointment
