import csv
import datetime
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os


class Analytics:
	def __init__(self):
		"""
        Initialise Analytics class with data from chat_data.csv
        """
		project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
		self.csv_file_path = os.path.join(project_root, "data", "chat_data", "chat_data.csv")
		self.data = self._read_data()

	def _read_data(self):
		"""
        Read data from CSV file and returns it as list of dictionaries
        Returns: list of dictionaries containing chat session data
        """
		data = []
		with open(self.csv_file_path, 'r', newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				row['start_time'] = datetime.strptime(row['start_time'], '%Y-%m-%d %H:%M:%S.%f')
				row['end_time'] = datetime.strptime(row['end_time'], '%Y-%m-%d %H:%M:%S.%f')
				row['key_themes'] = [theme.strip() for theme in row['key_themes'].split(',')]
				data.append(row)
		return data

	def generate_weekly_sessions_chart(self):
		"""
        Generates bar chart showing number of chat sessions per week
        """

		# Clear existing plots
		plt.close('all')

		# Group sessions by week
		weekly_sessions = defaultdict(int)

		for session in self.data:
			# Get the start of the week (Monday)
			start_date = session['start_time']
			# Get the Monday of the week
			week_start = start_date - timedelta(days=start_date.weekday())
			# Format as YYYY-MM-DD for Monday
			week_key = week_start.strftime('%Y-%m-%d')
			weekly_sessions[week_key] += 1

		# Sort weeks
		sorted_weeks = sorted(weekly_sessions.keys())
		counts = [weekly_sessions[week] for week in sorted_weeks]

		# Create bar chart
		plt.figure(figsize=(12, 6))
		plt.bar(sorted_weeks, counts, width=0.7)
		plt.xlabel('Week Starting Date')
		plt.ylabel('Number of Sessions')
		plt.title('Chat Sessions per Week')
		plt.xticks(rotation=45, ha='right')
		plt.tight_layout()

		plt.show()

	def generate_key_themes_chart(self, top_n=10):
		"""
        Generates a bar chart showing the frequency of key themes
        Args: top_n: Number of top themes to display, default is 10.
        """

		# Clear existing plots
		plt.close('all')

		# Collect all themes
		all_themes = []
		for session in self.data:
			all_themes.extend(session['key_themes'])

		# Count theme frequencies
		theme_counter = Counter(all_themes)

		# Get top N themes
		top_themes = theme_counter.most_common(top_n)
		themes, counts = zip(*top_themes) if top_themes else ([], [])

		# Create bar chart
		plt.figure(figsize=(12, 6))
		plt.bar(themes, counts, width=0.7)
		plt.xlabel('Key Themes')
		plt.ylabel('Frequency')
		plt.title(f'Top {top_n} Key Themes Frequency')
		plt.xticks(rotation=45, ha='right')
		plt.tight_layout()

		plt.show()

	def export_analytics_data_to_csv(self, top_n_themes):
		"""
	    Exports analytics data to CSV file containing number of sessions per week and common chat themes.
	    CSV file gets saved to 'data/analytics_exports' folder
	    Args: top_n_themes: Number of top themes to include, default is 10.
	    Returns: Path to the saved CSV file
	    """

		try:
			top_n_themes = int(top_n_themes)
		except ValueError:
			print("Invalid input. Please enter an integer.")
		else:
			project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
			export_dir = os.path.join(project_root, "data", "analytics_exports")
			os.makedirs(export_dir, exist_ok=True)

			# Generate filename (includes current date)
			current_date = datetime.now().strftime('%Y-%m-%d')
			export_filename = f"analytics_export_{current_date}_{top_n_themes}themes.csv"
			export_path = os.path.join(export_dir, export_filename)

			# Get data on number of sessions per week and common themes
			weekly_sessions = defaultdict(int)
			for session in self.data:
				start_date = session['start_time']
				week_start = start_date - timedelta(days=start_date.weekday())
				week_key = week_start.strftime('%Y-%m-%d')
				weekly_sessions[week_key] += 1
			sorted_weeks = sorted(weekly_sessions.keys())

			all_themes = []
			for session in self.data:
				all_themes.extend(session['key_themes'])
			theme_counter = Counter(all_themes)
			top_themes = theme_counter.most_common(top_n_themes)

			# Write data to CSV
			with open(export_path, 'w', newline='') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(['Data Type', 'Category', 'Value'])
				for week in sorted_weeks:
					writer.writerow(['Weekly Sessions', week, weekly_sessions[week]])
				writer.writerow([])
				for theme, count in top_themes:
					writer.writerow(['Theme Frequency', theme, count])

			print(f"\nAnalytics data exported to {export_path}")
			return export_path
