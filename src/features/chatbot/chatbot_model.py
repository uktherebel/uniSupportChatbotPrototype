from src.config.deepseek_api import client, response_settings
from src.features.chatbot.chatbot_config import base_system_prompt, appointment_booking_prompt
from src.features.chatbot.knowledge_base import KnowledgeBase
from src.features.appointment_booking.appointment_booking import AppointmentBookingSystem
from src.features.analytics.chat_transcript_analysis_model import extract_transcript_themes
from openai.types.chat import ChatCompletion
from sentence_transformers import SentenceTransformer, util
import torch
import os
import datetime
import csv

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Silence parallelism warning


class Chatbot:
	"""
	Chatbot class to facilitate students discussing wellbeing queries with UniSupport Bot.
	"""

	def __init__(self, user):
		"""
		Initialise chatbot with basic settings for chat interface (e.g. chatbot welcome message, user / chatbot message prefixes, exit keyword for user to type to end session, etc.) and empty message history / transcript.

		The Chatbot class has an association relationship with the Appointment Booking System class.

		"""

		self.user = user
		self.user_message_prefix = "User: "
		self.chatbot_response_prefix = "UniSupport Bot: "
		self.user_exit_keyword = "exit"
		self.chatbot_welcome_message = f"Welcome to UniSupport! How can I help you today?"
		self.chatbot_exit_message = "Goodbye!"
		self.message_history = []
		self.transcript = ""
		self.chat_active = False
		self.system_prompt = base_system_prompt + appointment_booking_prompt
		self.booking_status = ''
		self.chosen_appointment = None
		self.appointment_booking_system = AppointmentBookingSystem()  # There is an association relationship between the Chatbot class and the Appointment Booking System class
		self.start_time = None
		self.end_time = None
		self.knowledge_base = None
		self.transformer_model = None
		self.summary_texts = None
		self.summary_embeddings = None

	def user_message(self):
		"""
		Prompts user to enter a message and adds it to the message history / transcript. If the user types the exit keyword, the end_chat function is called to end the chat session.
		"""

		user_message = input('\n' + self.user_message_prefix).strip()

		self.add_message_to_history("user", user_message + '\n')
		if user_message.lower() == self.user_exit_keyword:
			self.end_chat()

	def chatbot_message(self):
		"""
		If the chat is active, this function generates a response from the API to the user's last message by calling generate_response; it then prints the API response to the console and adds it to the message history / transcript.
		"""

		if self.chat_active:
			try:
				chatbot_message = self.generate_response().strip()
				print('\n' + self.chatbot_response_prefix + chatbot_message)
				self.add_message_to_history("system", chatbot_message + '\n')
			except:
				print("")

	def generate_response(self):
		"""
		This function generates a response from the API to the user's last message using the system prompt and the full chat transcript so far.
		The response also takes parameters from response_settings which is in chatbot_config.py.
		Returns: contents of the API's response to the user's last message in the chat transcript.
		"""

		try:
			self.check_knowledge_base()

			api_response_full: ChatCompletion = client.chat.completions.create(messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": self.transcript}], **response_settings)
			api_response_message = api_response_full.choices[0].message.content

			if api_response_message == "<BOOK_APPOINTMENT>":
				self.book_appointment()
				after_booking_api_response_full: ChatCompletion = client.chat.completions.create(messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": self.transcript}], **response_settings)
				after_booking_api_response_message = after_booking_api_response_full.choices[0].message.content
				return after_booking_api_response_message

			else:
				return api_response_message

		except Exception as e:
			print(f"An error occurred while generating a response: {e}")

	def book_appointment(self):
		"""
		This function is called when the chatbot responds with the keyword '<BOOK_APPOINTMENT>'. It calls the appointment booking system to display available appointments and allow the user to select one, before returning to the chatbot to carry on with the conversation.
		Returns: booking status following the user using the Appointment Booking System.
		"""

		print('\n' + self.chatbot_response_prefix + "I'll help you book an appointment with our Wellbeing Staff. Let me show you the available time slots...")
		booking_result = self.appointment_booking_system.display_appointments(self.user)
		self.booking_status = booking_result[0]
		self.chosen_appointment = booking_result[1]
		self.add_message_to_history("system",
									f"AT THIS POINT IN THE CONVERSATION, THE USER WENT INTO THE APPOINTMENT BOOKING INTERFACE AND THEY RETURNED WITH THE FOLLOWING BOOKING STATUS: {self.booking_status}. THEY HAVE NOW RETURNED TO THE CHATBOT INTERFACE SO IN THE CHATBOT'S NEXT MESSAGE, IT SHOULD CARRY ON WITH THE CONVERSATION NATURALLY." + '\n')
		return self.booking_status

	def start_chat(self):
		"""
		This function starts the chat session by printing the welcome message and adding it to the message history / transcript.
		The function then runs a loop where the user is prompted for input, and chatbot responses are generated by the API.
		The loop ends if the user types the exit keyword (this is checked by the user_message function).
		This function also initialises the knowledge base & sets other relvant parameters such as the chat_active flag to True and sets the start time of the chat session.
		"""

		self.chat_active = True
		self.start_time = datetime.datetime.now()

		# Initialise knowledge base and transformer model (for cosine similarity used to extract relevant information from knowledge base when chatbot responds to user messages).
		self.knowledge_base = KnowledgeBase()
		self.transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
		self.summary_texts = list(self.knowledge_base.resource_summaries.values())
		self.summary_embeddings = self.transformer_model.encode(self.summary_texts, convert_to_tensor=True)

		# Add student's basic information to the chatbot's system prompt so that the chatbot can use this information when responding to student's messages.
		self.system_prompt += f"Here is some basic information about the Student you are talking to (feel free to use this information when talking to the student if appropriate): {self.user}"

		# Print the chatbot's welcome message and add it to the message history / transcript.
		print('\n' + self.chatbot_response_prefix + self.chatbot_welcome_message)
		self.add_message_to_history("system", self.chatbot_welcome_message + '\n')

		# Run loop of asking user to enter a message & then the chatbot responding to them.
		while self.chat_active:
			self.user_message()
			self.chatbot_message()

	def end_chat(self):
		"""
		This function ends the chat session by printing the exit message and adding it to the message history / transcript.
		Also sets other relvant parameters such as the chat_active flag to False and sets the end time of the chat session.
		The function also saves the chat session data to a CSV file in the data/chat_data folder for use by the Analytics System.
		"""

		# Set relvant parameters given that chat has ended, and print the chatbot's exit message.
		self.chat_active = False
		self.end_time = datetime.datetime.now()
		print('\n' + self.chatbot_response_prefix + self.chatbot_exit_message)
		self.add_message_to_history("system", self.chatbot_exit_message + '\n')

		# Calculate the session length & extract key themes from the chat transcript, for inclusion in the chat_data .csv file (used by Analytics system)
		session_length = self.end_time - self.start_time
		key_themes = extract_transcript_themes(self.transcript)
		session_id = 1

		# Save chat session data to .csv file in data/chat_data folder for use by Analytics System.
		base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
		csv_path = os.path.join(base_dir, "data/chat_data/chat_data.csv")

		try:
			with open(csv_path, "r") as file:
				csv_reader = csv.reader(file)
				session_ids = [int(row[0]) for row in csv_reader if row and row[0].isdigit()]
				if session_ids:
					session_id = max(session_ids) + 1
		except (FileNotFoundError, IndexError, ValueError):
			session_id = 1

		themes_str = ','.join(key_themes) if isinstance(key_themes, list) else str(key_themes)

		# Write the data processed above into the chat_data.csv file
		with open(csv_path, "a", newline='') as file:
			csv_writer = csv.writer(file)
			csv_writer.writerow([session_id, self.start_time, self.end_time, session_length, themes_str])
		return

	def add_message_to_history(self, role, content):
		"""
		This function is called each time a message is sent in order to add the message to the message history (list of messages sent) and the transcript (a string of all messages sent).
		Parameters: role (role of the actor sending the message e.g. user or chatbot / system), content (content of the message sent by the actor)
		"""
		self.message_history.append({"role": role, "content": content})
		self.transcript += f"{self.message_history[-1]['role']}: {self.message_history[-1]['content']}"

	def check_knowledge_base(self):
		"""
		Tries to determine the most relevant resource in the knowledge base that would help the student with their query.
		The function does this by comparing the user's last message to the summaries of resources in the knowldege base.
		It then reads the most relevant knowledge base resource / file into the system prompt so that the chatbot can make use of the information in that file when responding to the user's messages.
		"""

		# Convert last user message to embeddings
		last_user_message = self.message_history[-1]["content"]
		user_embedding = self.transformer_model.encode(last_user_message, convert_to_tensor=True)

		# Compute cosine similarity between user message embedding and embeddings for all knowledge base resource summaries
		cosine_scores = util.pytorch_cos_sim(user_embedding, self.summary_embeddings)

		# Find the best match
		best_match_idx = torch.argmax(cosine_scores)
		best_guide_filename = list(self.knowledge_base.resource_summaries)[best_match_idx]

		# Save path of the right resource document
		base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
		resource_file_path = os.path.join(base_dir, "data/knowledge_base", best_guide_filename)

		# Read the content of the best matching resource
		with open(resource_file_path, encoding='utf-8') as file:
			matching_resource = file.read()

		# Update system prompt to include the best matching resource so that the chatbot can use information from it when responding to the user's messages.
		self.system_prompt += f"If the content in the following wellbeing-related document may be relevant to the user based on the chat history, please use information from the document in your response.DOCUMENT: {matching_resource}"
