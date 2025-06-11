from pytest_bdd import scenarios, given, when, then, parsers
from data.appointments.appointments import appointments
from src.features.appointment_booking.appointment_booking import AppointmentBookingSystem
from src.models.users import Student

scenarios("appointment_booking.feature")
student_user = None
booking_system = None
test_appointments = None


# positive test case
@given('a student is logged in')
def student_logged_in():
	global student_user, booking_system, test_appointments
	student_user = Student(id=201, username="alee", name="Alice Lee", email="alee@example.com", password="password",
						   program="Computer Science", status="Active", booking_history=[]
						   )


@given('there is atleast one appointment available')
def appointments_from_data():
	global student_user, booking_system, test_appointments
	test_appointments = appointments


@when(
	parsers.parse('the student inputs "{valid_input:d}" to indicate that they want appointment one in the booking system')
)
def input_appointment_one(valid_input):
	global student_user, booking_system, test_appointments
	booking_system = AppointmentBookingSystem()
	booking_system.book_appointment(student_user, str(valid_input))


@then(
	parsers.parse('the booking system will add appointment "{valid_input:d}" to the student\'s booking history')
)
def notify_appointment_selected(valid_input):
	global student_user, booking_system, test_appointments
	assert booking_system.appointments[valid_input - 1] in student_user.booking_history


# negative test case
@given('a student is logged in')
def student_logged_in():
	global student_user, booking_system, test_appointments
	student_user = Student(id=201, username="alee", name="Alice Lee", email="alee@example.com", password="password",
						   program="Computer Science", status="Active", booking_history=[]
						   )


@given('there are only three appointments available')
def appointments_from_data():
	global student_user, booking_system, test_appointments
	test_appointments = appointments


@when(
	parsers.parse('the student inputs "{invalid_input:d}" to indicate that they want appointment four which is not available in the booking system')
)
def input_appointment_one(invalid_input):
	global student_user, booking_system, test_appointments
	booking_system = AppointmentBookingSystem()
	booking_system.book_appointment(student_user, str(invalid_input))


#
@then(
	parsers.parse('the booking system will notify user "{invalid_input:d}" is not associated with an available appointment')
)
def notify_appointment_selected(capsys, invalid_input):
	global student_user, booking_system, test_appointments
	booking_system.book_appointment(student_user, str(invalid_input))
	captured = capsys.readouterr()
	assert captured.out == '\nYou didn\'t enter a number associated with an appointment.\n'
