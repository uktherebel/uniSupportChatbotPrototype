from src.models.users import User, Student, WellBeingStaff, WellbeingManager

student1 = Student(
	id=201,
	username="alee",
	name="Alice Lee",
	email="alee@example.com",
	password="password",
	program="Computer Science",
	status="Active",
	booking_history=[]
)

student2 = Student(
	id=202,
	username="rpatel",
	name="Raj Patel",
	email="rpatel@example.com",
	password="password",
	program="Psychology",
	status="Active",
	booking_history=[]
)

student3 = Student(
	id=203,
	username="jchen",
	name="Jamie Chen",
	email="jchen@password.com",
	password="secure123",
	program="Business Administration",
	status="Active",
	booking_history=[]
)

wellbeing_staff1 = WellBeingStaff(
	id=101,
	username="dcohen",
	name="David Cohen",
	email="dcohen@example.com",
	password="password",
	appointment_availability=[],
	emergency_notifications=[]
)

wellbeing_staff2 = WellBeingStaff(
	id=102,
	username="lgarcia",
	name="Lisa Garcia",
	email="lgarcia@example.com",
	password="password",
	appointment_availability=[],
	emergency_notifications=[]
)

wellbeing_staff3 = WellBeingStaff(
	id=103,
	username="mjones",
	name="Melissa Jones",
	email="mjones@example.com",
	password="password",
	appointment_availability=[],
	emergency_notifications=[]
)

wellbeing_manager1 = WellbeingManager(
	id=301,
	username="jsmith",
	name="Jennifer Smith",
	email="jsmith@example.com",
	password="password"
)

wellbeing_manager2 = WellbeingManager(
	id=302,
	username="kthomas",
	name="Kyle Thomas",
	email="kthomas@example.com",
	password="password"
)

wellbeing_manager3 = WellbeingManager(
	id=303,
	username="sbaker",
	name="Sarah Baker",
	email="sbaker@example.com",
	password="password"
)

users_list = [
	student1, student2, student3,
	wellbeing_staff1, wellbeing_staff2, wellbeing_staff3,
	wellbeing_manager1, wellbeing_manager2, wellbeing_manager3
]

users = {u.email: u for u in users_list}
