import time
import os


def startup_animation():
	"""
	Prints the contents of the startup animation file line by line.
	"""
	delay = 0.02
	try:
		# Open and read startup animation file
		current_dir = os.path.dirname(os.path.abspath(__file__))
		animation_file = os.path.join(current_dir, 'startup_animation_string.txt')

		with open(animation_file, 'r', encoding='utf-8') as file:
			lines = file.readlines()

		# Print each line of the file
		for line in lines:
			print(line, end='')
			time.sleep(delay)

		print(f"\n{'*' * 21}\nWelcome to UniSupport!\n{'*' * 21}\n\nPlease login to continue")

	except FileNotFoundError:
		print(f"Error: Startup animation file not found.")
	except Exception as e:
		print(f"An error occurred with startup animation: {e}")
