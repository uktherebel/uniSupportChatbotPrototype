from src.utils.startup_animation.startup_animation import startup_animation
from src.utils.auth.login import login
from src.features.appointment_booking.appointment_booking import AppointmentBookingSystem
from src.features.analytics.analytics_model import Analytics
from data.users.users import users, users_list
from src.features.chatbot.knowledge_base import KnowledgeBase


class App:
	"""
	App class which is the starting point for all system usage
	"""

	def __init__(self):
		self.welcome_message = "Welcome to UniSupport!"
		self.login_message = "Please login to continue:"
		self.login_failed_message = "Login failed. Please try again."
		self.current_user = None
		self.login_success_message = "Log in successful!"
		self.appointment_booking_system = AppointmentBookingSystem()

		self.debug_mode = False

	def run(self, run_animation=True):
		"""
		Start the application by running login sequence; if login successful, user goes to menu. If login failed, user is prompted to try again.
		"""

		self.current_user = None

		if self.debug_mode == False:
			if run_animation:
				startup_animation()
			self.login()
			print(f"\n{'*' * len(self.welcome_message)}")
			print(f"{self.welcome_message}")
			print(f"{'*' * len(self.welcome_message)}")
			print(f"\n{self.login_message}")
			self.menu()

		elif self.debug_mode == True:
			debug_user = int(input("\nType 1 to login as Student\nType 2 to login as Wellbeing Staff\nType 3 to login as Wellbeing Manager\n\nChoice: ").strip())
			if debug_user == 1:
				for u in users_list:
					if u.role == "student":
						self.current_user = u
						break
			if debug_user == 2:
				for u in users_list:
					if u.role == "wellbeing_staff":
						self.current_user = u
						break
			if debug_user == 3:
				for u in users_list:
					if u.role == "wellbeing_manager":
						self.current_user = u
						break
			self.menu()

	def menu(self):
		"""
		Menu function to get user input on what they want to do / what actor they are e.g. student, wellbeing staff, etc.
		"""

		while True:
			print(f'\nChoose an option from the menu below:')

			if self.current_user.role == "student":
				try:
					choice = int(input(f"\n1. Start chatbot session"
									   f"\n2. Manage your appointments"
									   f"\n3. View your notifications"
									   f"\n4. Logout"
									   f"\n5. Close Application"
									   "\n\nEnter your choice: ").strip())
				except:
					print("\nInvalid input. Please try again.")
					continue
				if choice not in [1, 2, 3, 4, 5]:
					print("\nInvalid input. Please try again.")
				if choice == 1:
					print("\nStarting chatbot session...")
					print("\nPlease note that the chatbot takes a few seconds to think before responding to your messages.")
					print("\nType 'exit' at any point to end the chat session and return to the main menu.")
					self.current_user.start_chatbot_session()
					continue
				if choice == 2:
					print("\nManaging your appointments...")
					self.current_user.modify_appointment(self.appointment_booking_system)
					continue
				if choice == 3:
					print("\nViewing notifications...")
					notifications = self.current_user.notifications
					if not notifications:
						print("\nYou have no notifications.")
						continue
					elif notifications:
						for n in self.current_user.notifications:
							print(f"\n{n.subject}: {n.message}")
					continue
				if choice == 4:
					print("\nLogging out...")
					print(f"\n{self.login_message}")
					self.run(run_animation=False)
					break
				if choice == 5:
					print("\nExiting...")
					break
				continue

			elif self.current_user.role == "wellbeing_staff":
				try:
					choice = int(input(f"\n1. Manage your appointments"
									   f"\n2. Manage chatbot knowledge base"
									   f"\n3. View your notifications"
									   f"\n4. Logout"
									   f"\n5. Close Application"
									   "\n\nEnter your choice: ").strip())
				except:
					print("\nInvalid input. Please try again.")
					continue
				if choice not in [1, 2, 3, 4, 5]:
					print("\nInvalid input. Please try again.")
				if choice == 1:
					print("\nManaging your appointments...")
					self.current_user.manage_appointments(self.appointment_booking_system)
				if choice == 2:
					while True:
						try:
							choice = int(input(f"\n1. View knowledge base resources"
											   f"\n2. Upload knowledge base resource"
											   f"\n3. Delete knowledge base resource"
											   f"\n4. Exit"
											   "\n\nEnter your choice: ").strip())
						except:
							print("\nInvalid input. Please try again.")
							continue
						if choice not in [1, 2, 3, 4]:
							print("\nInvalid input. Please try again.")
						if choice == 1:
							self.current_user.view_resources()
							continue
						if choice == 2:
							while True:
								filename, summary, content = input("\nEnter filename: "), input("\nEnter summary: "), input("\nContent: ")
								if filename in KnowledgeBase.files_record or filename in KnowledgeBase.resource_summaries:
									print(f"\n{filename} is already present.")
									break
								else:
									self.current_user.add_resource(filename, summary, content)
									break
						if choice == 3:
							self.current_user.view_resources()
							filename = input("\nEnter the filename to delete: ")
							if filename in KnowledgeBase.files_record:
								self.current_user.remove_resource(filename)
								print("\nFile deleted! Knowledge base updated.")
								continue
							else:
								print("\nFile not found.")
								continue
						if choice == 4:
							break
						continue
					continue
				if choice == 3:
					print("\nViewing notifications...")
					notifications = self.current_user.notifications
					if not notifications:
						print("\nYou have no notifications.")
						continue
					elif notifications:
						for n in self.current_user.notifications:
							print(f"\n{n.subject}: {n.message}")
					continue
				if choice == 4:
					print("\nLogging out...")
					self.run(run_animation=False)
					break
				if choice == 5:
					print("\nExiting...")
					break
				continue
			elif self.current_user.role == "wellbeing_manager":
				try:
					choice = int(input(f"\n1. Go to analytics dashboard"
									   f"\n2. Logout"
									   f"\n3. Close Application"
									   "\n\nEnter your choice: ").strip())
				except:
					print("\nInvalid input. Please try again.")
					continue
				if choice not in [1, 2, 3, 4]:
					print("\nInvalid input. Please try again.")
				if choice == 1:
					analytics = Analytics()
					while True:
						try:
							choice = int(input(f"\n1. View data on # chatbot sessions over time"
											   f"\n2. View data on common chatbot topics"
											   f"\n3. Export data as .csv file"
											   f"\n4. Exit"
											   "\n\nEnter your choice: ").strip())
						except:
							print("\nInvalid input. Please try again.")
							continue
						if choice not in [1, 2, 3, 4, 5]:
							print("\nInvalid input. Please try again.")
						if choice == 1:
							analytics.generate_weekly_sessions_chart()
							continue
						if choice == 2:
							analytics.generate_key_themes_chart()
							continue
						if choice == 3:
							n_themes = input("\nEnter the number of themes you want in the CSV export: ")
							analytics.export_analytics_data_to_csv(n_themes)
						if choice == 4:
							break
						continue
					continue
				if choice == 2:
					print("\nLogging out...")
					self.run(run_animation=False)
					break
				if choice == 3:
					print("\nExiting...")
					break
				continue

	def login(self):
		"""
		Allow a user to login with email address & password; check their credentials and if correct return True & sets current_user to student object
		:return: Returns user object if credentials are correct, otherwise gives login failed message and prompts user to try again
		"""
		while True:
			login_result = login()
			if login_result:
				self.current_user = login_result
				print(f"\n{self.login_success_message}")
				print(f"\nHi, {self.current_user.username}!")
				break
			else:
				print(f"\n{self.login_failed_message}")


if __name__ == "__main__":
	app = App()
	app.run()
