import os


class KnowledgeBase:
	initial_resource_summaries = {
		"campus_safety.txt": "A detailed guide to personal security, offering advice on staying safe on and off campus, preventing harassment, and responding to potential emergencies.",
		"disabilities.txt": "A guide explaining the university's approach to supporting students with disabilities, detailing rights, accommodations, and resources for inclusive education.",
		"extenuating_circumstances.txt": "A thorough explanation of how students can seek academic support that may affect their performance in exams, coursework, etc. during unexpected challenging life events, including process, documentation, and available accommodations.",
		"health_and_welfare.txt": "An extensive overview of physical and mental health strategies, covering nutrition, financial well-being, personal safety, and holistic student welfare.",
		"mental_health.txt": "A comprehensive resource providing strategies for managing mental health challenges, recognizing warning signs, and accessing support during university life."
	}
	resource_summaries = {}
	files_record = ""
	resources_path = ""

	# Constructor for Class Attributes. Called at the bottom after Class definition.
	@staticmethod
	def init_knowledge_base():
		KnowledgeBase.resources_path = KnowledgeBase.get_resources_path()
		KnowledgeBase.resource_summaries = KnowledgeBase.initial_resource_summaries.copy()

	@staticmethod
	def update_files_record():
		KnowledgeBase.files_record = sorted(os.listdir(KnowledgeBase.resources_path))

	@staticmethod
	def view_files():
		for i, item in enumerate(KnowledgeBase.resource_summaries, 1):
			print(f"\n{i}.Filename:'{item}', Summary: {KnowledgeBase.resource_summaries[item]}")

	@staticmethod
	def add_file(filename, summary, content):
		# Ensure filename has .txt extension
		if not filename.endswith('.txt'):
			filename = filename + '.txt'

		KnowledgeBase.resource_summaries[filename] = summary
		new_file = os.path.join(KnowledgeBase.resources_path, filename)

		with open(new_file, 'w') as f:
			f.write(content)

		# Update variable holding the filenames in the folder
		KnowledgeBase.update_files_record()

	@staticmethod
	def remove_file(filename):
		try:
			# Ensure filename has .txt extension
			if not filename.endswith('.txt'):
				filename = filename + '.txt'

			# Check if the file exists in memory before removing
			if filename in KnowledgeBase.resource_summaries:
				del KnowledgeBase.resource_summaries[filename]

			file_path = os.path.join(KnowledgeBase.resources_path, filename)
			if os.path.exists(file_path):
				os.remove(file_path)
			else:
				raise Exception(f"File {filename} not found.")
		except Exception as e:
			raise Exception(f"Error while deleting file {filename}: {str(e)}")

		# Update variable holding the filenames in the folder
		KnowledgeBase.update_files_record()

	@staticmethod
	def get_resources_path():
		base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
		resources_file_path = os.path.join(base_dir, "data/knowledge_base")

		return resources_file_path


KnowledgeBase.init_knowledge_base()
