from datetime import datetime
from src.models.appointment import Appointment
from src.models.notification import Notification
from data.appointments.appointments import appointments
from data.users.users import users_list as users_list


class AppointmentBookingSystem:
	_instance = None

	# The Appointment Booking System follows the 'Singleton Design Pattern' in order to ensure that there is a consistent record of appointments that have been booked / that are available to be booked
	# The 'Publisher Subscriber Design Pattern' is used to send notifications to the relevant users when an appointment gets booked

	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(AppointmentBookingSystem, cls).__new__(cls)
			cls._instance.appointments = []

			# this nested loop matches practitioner names with users that have a role of wellbeing staff and match the name of the practitioner the name is replaced by the actual WellbeingStaff(User) object
			for appt in appointments:
				for u in users_list:
					if u.role == 'wellbeing_staff' and appt.participants['practitioner'] == u.name:
						appt.participants['practitioner'] = u
						cls._instance.appointments.append(appt)
						break
			cls._instance.waiting_list = [{'student_id': 1113456}]
		return cls._instance

	def _get_available_appointments(self):
		"""
		This function creates a list of available appointments
		:return: list of available appointments
		"""

		return [appt for appt in self.appointments if not appt.booked]

	def display_appointments(self, current_user):
		"""
		Displays all available appointments
		"""

		available = self._get_available_appointments()
		for idx, item in enumerate(available, start=1):
			# this selects only items that are available (i.e. not booked).
			if not item.booked:
				print(
					f"\n{idx}) Date: {item.date.strftime('%d/%m/%Y')} "
					f"| Time: {item.time.strftime('%H:%M')} "
					f"| Location: {item.location} "
					f"| Practitioner: {item.participants['practitioner'].name}"
				)
		selection = input(
			"\nPlease type the number of the appointment you want to book. Or type 'None' if you want to be added to waiting list: ")
		booking_status = self.book_appointment(current_user, selection, available)
		return booking_status

	def book_appointment(self, current_user, selection, available=None):
		"""
		Process of booking an appointment and confirming email address for confirmation to be sent to
		"""

		if not available:
			available = self._get_available_appointments()

		if selection.lower().strip() == 'none':
			self.add_waiting_list(current_user)
			return ('Waiting List', None)
		else:
			try:
				chosen_appointment = available[int(selection) - 1]
			except ValueError:
				# catches errors where they don't type None or a number
				print("\nYou didn't enter a number.")
				return (None, None)
			except IndexError:
				# catches errors where they type a number, but it's not a number linked to an appointment.
				print("\nYou didn't enter a number associated with an appointment.")
				return (None, None)
			else:
				print('\nThank you for choosing a booking.')

				if self.validate_appointment(chosen_appointment) and not chosen_appointment.booked:
					for appt in self.appointments:
						if appt == chosen_appointment:
							appt.booked = True
					chosen_appointment.participants['attendee'] = current_user
					current_user.booking_history.append(chosen_appointment)

					student_notification = Notification(
						'New appointment',
						f"You have a new appointment on {chosen_appointment.date.strftime('%d/%m/%Y')} "
						f"at {chosen_appointment.time.strftime('%H:%M')} at {chosen_appointment.location}.")
					self.send_notification(current_user, student_notification)

					wellbeing_staff = chosen_appointment.participants['practitioner']
					staff_notification = Notification(
						'New appointment',
						f"Student {current_user.id} has made a new appointment with you on {chosen_appointment.date.strftime('%d/%m/%Y')} "
						f"at {chosen_appointment.time.strftime('%H:%M')} at {chosen_appointment.location}.")
					self.send_notification(wellbeing_staff, staff_notification)

					print(
						'\nYour booking has been confirmed. You should receive a notification with your booking confirmation.')
					return ('Booked', chosen_appointment)

				else:
					print('\nSorry, this booking has now been taken. Please choose a different appointment.')
					self.display_appointments(current_user)

	def add_waiting_list(self, current_user):
		"""
		Add student to waiting list immediately without further prompts
		"""

		self.waiting_list.append({'student_id': current_user.id})
		print("\nYou have been added to the waiting list.")

		# Sends a notification to a wellbeing_staff member. There may be a better way to do this (a universal waiting_list that all wellbeing staff can access?)
		notification = Notification(
			'Student added to waiting list',
			f"Student {current_user.id} has been added to the waiting list for an appointment.")
		self.send_notification_to_wellbeing_staff(notification)

	def validate_appointment(self, appointment):
		"""Checks that appointment is still available at time of confirming the booking."""

		return not appointment.booked

	def cancel_appointment(self, appointment):
		"""Sets appointment to be available again - changes booked value from True to False and removes student from attendees."""

		for i in self.appointments:
			if i == appointment:
				i.booked = False
				i.participants['attendee'] = None

	def create_appointment(self, current_user):
		"""
		Creates a new appointment and adds it to the appointment list
		"""

		create_appointment = False
		while not create_appointment:
			try:
				date = datetime.strptime(input("Please enter date of appointment YYYY/MM/DD: "), '%Y/%m/%d')
			except ValueError:
				print("You didn't enter a date in the correct format.")
				continue
			try:
				time = datetime.strptime(input("Please enter time of appointment HH:MM: "), '%H:%M')
				time = time.time()  # converts to a time object
			except ValueError:
				print("You didn't enter a time in the correct format.")
				continue
			location = input("Please enter location of appointment: ")
			appointment = Appointment(date, time, location, {'practitioner': current_user.name, 'attendee': None}, False)
			self.appointments.append(appointment)
			create_appointment = True

	def send_notification(self, recipient, notification):
		"""
		Adds notification object to recipient's notification list
		"""

		recipient.notifications.append(notification)

	def send_notification_to_wellbeing_staff(self, notification):
		"""
		Function to broadcast a notification to all wellbeing staff in case student added to waiting list.
		'Publisher Subscriber Design Pattern' is used to send notifications to the relevant users when an appointment gets booked
		"""

		for u in users_list:
			if u.role == 'wellbeing_staff':
				u.notifications.append(notification)
