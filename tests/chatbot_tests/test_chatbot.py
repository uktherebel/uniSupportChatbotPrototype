import os
from pytest_bdd import scenarios, given, when, then
from src.models.users import WellBeingStaff

scenarios('chatbot.feature')
wellbeing_staff_user = None
test_project_root = None
test_export_dir = None


# positive test case
@given('a wellbeing staff member is logged in')
def wellbeing_staff_logged_in():
	global wellbeing_staff_user, test_project_root, test_export_dir
	wellbeing_staff_user = WellBeingStaff(
		id=101,
		username="dcohen",
		name="David Cohen",
		email="dcohen@example.com",
		password="password",
		appointment_availability=[],
		emergency_notifications=[]
	)


@when('the wellbeing staff member adds a new file to the knowledge bank')
@when('the filename is 15 characters long')
@when('the filename is not already in use')
def new_file_fifteen_characters():
	global wellbeing_staff_user, test_project_root, test_export_dir
	wellbeing_staff_user.add_resource('abcdefghijklmnop', 'this is a summary', 'this is some content')


@then('the file is added to the knowledge bank')
def file_added():
	global wellbeing_staff_user, test_project_root, test_export_dir
	test_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
	test_export_dir = os.path.join(test_project_root, "data", "knowledge_base")
	os.makedirs(test_export_dir, exist_ok=True)
	assert os.path.isfile(os.path.join(test_export_dir, 'abcdefghijklmnop.txt'))


# negative test case
@given('a wellbeing staff member is logged in')
def wellbeing_staff_logged_in():
	global wellbeing_staff_user
	wellbeing_staff_user = WellBeingStaff(
		id=101,
		username="dcohen",
		name="David Cohen",
		email="dcohen@example.com",
		password="password",
		appointment_availability=[],
		emergency_notifications=[]
	)


@when('the wellbeing staff member adds a new file to the knowledge bank')
@when('the filename is 26 characters long')
@when('the filename is not already in use')
def new_file_twenty_six_characters():
	global wellbeing_staff_user
	wellbeing_staff_user.add_resource('abcdefghijklmnopqrstuvwxyz', 'this is a summary', 'this is some content')


@then('the system will notify the user that filename is too long')
def file_added(capsys):
	global wellbeing_staff_user
	wellbeing_staff_user.add_resource('abcdefghijklmnopqrstuvwxyz', 'this is a summary', 'this is some content')
	captured = capsys.readouterr()
	assert captured.out == 'Filename length is too long. Needs to be 20 or fewer characters.\n'
