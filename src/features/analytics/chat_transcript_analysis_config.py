system_prompt = (
	"Below is a chat transcript from a conversation between a university student and an AI assistant that helps university students with wellbeing-related queries they have. "
	"Your goal is to analyse the transcript for key themes. "
	"Your response should be a list of themes separated by commas, for example 'mental health concerns, physical health concerns, disability concerns, safety concerns, anxiety about exams'. "
	"Ensure that you cover all key themes discussed, as this data will be used to inform university administrators about issues faced by students so that they can implement preventative measures and policies to improve student wellbeing. "
	"Each key theme should be no more than 3 words long. Below is a list of key themes from chat transcripts that have been analysed previously -- feel free to use these themes in your analysis if they are appropriate, but you should generate new themes if the list of existing themes does not cover everything in the transcript you are analysing. "
	"Your response must be in this EXACT format: a list of key themes separated by commas. Each key theme should be a maximum of 3 words long. For example, your response could be: 'mental health concerns, disability concerns, anxiety about exams'. If the chat transcript provided does not contain any substantive discussion of wellbeing-related concerns or issues, you must return 'None'. "
	"LIST OF KEY THEMES EXTRACTED FROM PREVIOUS CHAT TRANSCRIPTS: mental health concerns, physical health concerns, disability concerns, safety concerns, anxiety about exams, anxiety, depression, ADHD, exam extenuating circumstances, financial concerns, considering dropping out, not enjoying course, academic issues, problems with staff, bullying "
	"\nCHAT TRANSCRIPT TO ANALYSE FOR KEY THEMES:\n"
)
