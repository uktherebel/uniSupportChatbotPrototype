from datetime import datetime, time


class Appointment:
	def __init__(self, date: datetime, time: time, location, participants: dict, booked: bool):
		self.date = date
		self.time = time
		self.location = location
		self.participants = participants
		self.booked = booked
