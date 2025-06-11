from openai import OpenAI

api_key = ""
base_url = "https://api.deepseek.com"
client = OpenAI(api_key=api_key, base_url=base_url)

response_settings = {
	"model": "deepseek-chat",
	"stream": False,
	"temperature": 1,
	"frequency_penalty": 1}
