from src.config.deepseek_api import client, response_settings
from src.features.analytics.chat_transcript_analysis_config import system_prompt
from openai.types.chat import ChatCompletion


def extract_transcript_themes(transcript):
	"""
	This function generates a list of key themes extracted from a chat transcript between the UniSupport bot and a student.
	Returns: comma separated list of strings; each string is a key theme from the transcript
	"""

	api_response_full: ChatCompletion = client.chat.completions.create(messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": transcript}], **response_settings)
	key_themes = api_response_full.choices[0].message.content

	if key_themes == "None":
		return []
	key_themes = key_themes.split(",")
	for theme in key_themes:
		theme = theme.strip()
		if theme == "":
			key_themes.remove(theme)
	return key_themes
