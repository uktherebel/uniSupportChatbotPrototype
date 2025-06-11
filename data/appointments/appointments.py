from src.models.appointment import Appointment
from datetime import datetime, time

appointments = [
	Appointment(
		datetime(2025, 8, 8),
		time(14, 30),
		'Room 11, CS Building',
		{'practitioner': 'Lisa Garcia', 'attendee': None},
		False
	),
	Appointment(
		datetime(2025, 9, 3),
		time(10, 0),
		'Room 15, CS Building',
		{'practitioner': 'Lisa Garcia', 'attendee': None},
		False
	),
	Appointment(
		datetime(2025, 11, 14),
		time(9, 30),
		'Room 7, CS Building',
		{'practitioner': 'David Cohen', 'attendee': None},
		False
	),
]
