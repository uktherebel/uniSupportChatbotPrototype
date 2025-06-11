from data.users.users import users


def login():
	"""
	Allow a user to login with email address & password; check their credentials and if correct return True & sets current_user to student object
	Returns: user object if credentials are correct, False otherwise
	"""
	email = input(f"\nEmail: ").strip().lower()
	password = input(f"\nPassword: ").strip()

	if email not in users.keys():
		return False
	else:
		user_object = users[email]
		if user_object.password == password:
			return user_object
		else:
			return False
