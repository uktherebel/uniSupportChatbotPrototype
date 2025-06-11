from dataclasses import dataclass
from datetime import datetime, time
from src.features.chatbot.knowledge_base import KnowledgeBase
from src.models.notification import Notification


# The 'Inheritance Design Pattern' is used, as Students, Wellbeing Staff & Wellbeing Managers inherit from the User class

@dataclass
class User:
	def __init__(self, id, username, name, email, password, role, notifications):
		self.id = id
		self.username = username
		self.name = name
		self.email = email
		self.password = password
		self.role = role
		self.notifications = []


@dataclass
class Student(User):
	def __init__(self, id, username, name, email, password, program, status, booking_history):
		super().__init__(id, username, name, email, password, role='student', notifications=[])
		self.program = program
		self.status = status
		self.booking_history = []

	def __repr__(self):
		return f"Student(id={self.id}, username={self.username}, name={self.name}, email={self.email}, password={self.password}, program={self.program}, status={self.status}, booking_history={self.booking_history})"

	def start_chatbot_session(self):
		from src.features.chatbot.chatbot_model import Chatbot
		chatbot = Chatbot(self)
		chatbot.start_chat()

	def display_booking_history(self):
		"""
		Displays the booking history of a student
		"""

		if not self.booking_history:
			print("You have no booking history.")
		else:
			for booking in self.booking_history:
				print(f"Date: {booking.date.strftime('%d/%m/%Y')} | Time: {booking.time.strftime('%H:%M')} | Location: {booking.location} | Practitioner: {booking.participants['practitioner']}")

	def modify_appointment(self, appointment_booking_system):
		"""
		Allows student to cancel or reschedule their appointment
		"""

		# Filter for only future appointments
		future_appointments = [appt for appt in self.booking_history
							   if datetime.combine(appt.date, appt.time) > datetime.now()]

		if not future_appointments:
			print("\nYou don't have any upcoming appointments to modify.")
			return

		print("\nYour upcoming appointments:")
		for idx, appointment in enumerate(future_appointments, start=1):
			print(
				f"\n{idx}) Date: {appointment.date.strftime('%Y-%m-%d')} | Time: {appointment.time.strftime('%H:%M')} | Location: {appointment.location}")

		try:
			selection = int(input("\nSelect the number of the appointment you want to modify: ")) - 1
			selected_appointment = future_appointments[selection]
		except (ValueError, IndexError):
			print("\nInvalid selection.")
			return

		print("\nWould you like to:")
		print("1) Cancel the appointment")
		print("2) Reschedule the appointment")
		choice = input("\nEnter 1 or 2: ").strip()

		if choice == '1':
			# Cancel appointment from student record. Then run cancel_appointment function in booking system to update appointments list
			self.booking_history.remove(selected_appointment)
			appointment_booking_system.cancel_appointment(selected_appointment)

			# Send cancellation notification
			notification = Notification(
				'Appointment cancelled',
				f"Your appointment on {selected_appointment.date.strftime('%d/%m/%Y')} "
				f"at {selected_appointment.time.strftime('%H:%M')} at {selected_appointment.location} "
				f"has been cancelled."
			)
			self.notifications.append(notification)

			print("\nYour appointment has been cancelled.")


		elif choice == '2':
			# Put the appointment back into the system, then allows student to pick another booking.
			self.booking_history.remove(selected_appointment)
			appointment_booking_system.cancel_appointment(selected_appointment)

			# Send reschedule notification
			notification = Notification(
				'Appointment rescheduled',
				f"Your appointment on {selected_appointment.date.strftime('%d/%m/%Y')} "
				f"at {selected_appointment.time.strftime('%H:%M')} at {selected_appointment.location} "
				f"is being rescheduled."
			)
			self.notifications.append(notification)

			print("\nLet's reschedule your appointment:")
			appointment_booking_system.display_appointments(self)

		else:
			print("\nInvalid choice. No changes made.")


@dataclass
class WellBeingStaff(User):
	def __init__(self, id, username, name, email, password, appointment_availability, emergency_notifications):
		super().__init__(id, username, name, email, password, role='wellbeing_staff', notifications=[])
		self.appointment_availability = []
		self.emergency_notifications = []

	def __repr__(self):
		return f"WellBeingStaff(id={self.id}, username={self.username}, name={self.name}, email={self.email}, password={self.password}, appointment_availability={self.appointment_availability}, emergency_notifications={self.emergency_notifications})"

	@staticmethod
	def view_resources():
		KnowledgeBase.view_files()

	@staticmethod
	def add_resource(filename, summary, content):
		if len(filename) > 20:
			print("Filename length is too long. Needs to be 20 or fewer characters.")
		else:
			KnowledgeBase.add_file(filename, summary, content)
			print("\nNew file saved! Knowledge base updated.")

	@staticmethod
	def remove_resource(filename):
		KnowledgeBase.remove_file(filename)

	def create_appointment(self, appointment_booking_system):
		appointment_booking_system.create_appointment(self)

	def manage_appointments(self, appointment_booking_system):
		future_appointments = [appt for appt in appointment_booking_system.appointments
							   if appt.participants.get('practitioner').id == self.id and appt.booked == True]

		if not future_appointments:
			print('\nYou do not have any upcoming appointments to manage.')
			return

		print("\nYour upcoming appointments:")
		for idx, appointment in enumerate(future_appointments, start=1):
			print(
				f"{idx}) Date: {appointment.date.strftime('%Y-%m-%d')} | Time: {appointment.time.strftime('%H:%M')} | Location: {appointment.location}")

		try:
			selection = int(input("\nSelect the number of the appointment you want to modify: ")) - 1
			selected_appointment = future_appointments[selection]
		except (ValueError, IndexError):
			print("\nInvalid selection.")
			return

		print("\nWould you like to:")
		print("1) Cancel a booked appointment")
		print("2) Delete an available appointment")
		print("3) Reschedule the appointment")
		choice = input("\nEnter 1, 2, or 3: ").strip()

		if choice == '1':
			if not selected_appointment.booked:
				print('This appointment is not booked.')
				return

			student = selected_appointment.participants['attendee']

			appointment_booking_system.delete_appointment(selected_appointment)

			notification = Notification(
				'Appointment cancelled by staff',
				f"Your appointment on {selected_appointment.date.strftime('%d/%m/%Y')} at "
				f"{selected_appointment.time.strftime('%H:%M')} at {selected_appointment.location} was cancelled."
			)

			appointment_booking_system.send_notification(student, notification)

			print("\nThe chosen appointment has been cancelled and the attendee has been notified.")

		elif choice == '2':
			if selected_appointment.booked:
				print('\nThis appointment has already been booked and cannot be deleted from here. Please cancel the appointment from the main menu.')

			appointment_booking_system.delete_appointment(selected_appointment)
			print("\nThe chosen appointment has been deleted from the system.")

		elif choice == '3':
			print("\nWould you like to:")
			print("1) Change the date of the selected appointment")
			print("2) Change the time of the selected appointment")
			print("3) Change the location of the selected appointment")

			reschedule = input("\nEnter 1, 2, or 3: ").strip()

			if reschedule == '1':
				try:
					date = datetime.strptime(input("\nPlease enter date of appointment YYYY/MM/DD: "), '%Y/%m/%d')
					selected_appointment.date = date
					print(f'\nThe appointment date has been successfully updated to {date}.')
				except ValueError:
					print("\nYou didn't enter a date in the correct format.")
					return

			elif reschedule == '2':
				try:
					time = datetime.strptime(input("\nPlease enter time of appointment HH:MM: "), '%H:%M')
					time = time.time()  # converts to a time object
					selected_appointment.time = time
					print(f'\nThe appointment time has been successfully updated to {time}.')

				except ValueError:
					print("\nYou didn't enter a time in the correct format.")

			elif reschedule == '3':
				try:
					location = input('\nPlease enter the new location of the appointment: ')
					selected_appointment.location = location
					print(f'\nThe appointment location has been successfully updated to {location}.')
				except Exception as e:
					print(f'\nThe following exception has occurred: {e}')

			if selected_appointment.booked:
				student = selected_appointment.participants['attendee']
				notification = Notification(
					'Appointment rescheduled by staff',
					f"Your new appointment details are: {selected_appointment.date.strftime('%d/%m/%Y')} at "
					f"{selected_appointment.time.strftime('%H:%M')} at {selected_appointment.location}."
				)

				appointment_booking_system.send_notification(student, notification)

	def update_availability(self, appointment_booking_system):
		print('Please enter the following details to create an appointment:')
		appointment = appointment_booking_system.create_appointment(self)
		print('The appointment has been created with these details.')
		self.appointment_availability.append(appointment)


@dataclass
class WellbeingManager(User):
	def __init__(self, id, username, name, email, password):
		super().__init__(id, username, name, email, password, role='wellbeing_manager', notifications=[])

	def __repr__(self):
		return f"WellbeingManager(id={self.id}, username={self.username}, name={self.name}, email={self.email}, password={self.password})"
