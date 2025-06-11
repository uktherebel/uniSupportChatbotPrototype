import os
from datetime import datetime
from pytest_bdd import scenarios, given, when, then, parsers
from src.features.analytics.analytics_model import Analytics
from src.models.users import WellbeingManager

scenarios('analytics.feature')
wellbeing_officer_user = None
dashboard = None
test_project_root = None
test_export_dir = None
current_date = None
result = None


# positive test case
@given('a wellbeing officer is logged in')
def wellbeing_officer_logged_in():
	global wellbeing_officer_user, dashboard, test_project_root, test_export_dir, current_date, result
	wellbeing_officer_user = WellbeingManager(
		id=301,
		username="jsmith",
		name="Jennifer Smith",
		email="jsmith@example.com",
		password="password"
	)


@when(
	parsers.parse('the wellbeing officer inputs "{themes:d}" as the desired number of trends when exporting data to a csv file')
)
def csv_file_eight_trends(themes):
	global wellbeing_officer_user, dashboard, test_project_root, test_export_dir, current_date, result
	dashboard = Analytics()
	result = dashboard.export_analytics_data_to_csv(themes)


@then(
	parsers.parse('a csv file is created with the filename showing there are "{themes:d}" themes')
)
def file_added(themes):
	global wellbeing_officer_user, dashboard, test_project_root, test_export_dir, current_date, result
	test_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
	test_export_dir = os.path.join(test_project_root, "data", "analytics_exports")
	os.makedirs(test_export_dir, exist_ok=True)
	current_date = datetime.now().strftime('%Y-%m-%d')
	assert result == os.path.join(test_export_dir, f"analytics_export_{current_date}_{themes}themes.csv")


# negative test case
@given('a wellbeing officer is logged in')
def wellbeing_officer_logged_in():
	global wellbeing_officer_user, dashboard
	wellbeing_officer_user = WellbeingManager(
		id=301,
		username="jsmith",
		name="Jennifer Smith",
		email="jsmith@example.com",
		password="password"
	)


@when('the wellbeing officer inputs yes as the desired number of trends when exporting data to a csv file')
def csv_file_eight_trends():
	global wellbeing_officer_user, dashboard
	dashboard = Analytics()
	dashboard.export_analytics_data_to_csv('yes')


@then('the analytics system will notify the user that they have entered an invalid input')
def file_added(capsys):
	global wellbeing_staff_user, dashboard
	dashboard.export_analytics_data_to_csv('yes')
	captured = capsys.readouterr()
	assert captured.out == 'Invalid input. Please enter an integer.\n'
