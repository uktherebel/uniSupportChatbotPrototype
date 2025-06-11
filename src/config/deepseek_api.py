from openai import OpenAI

api_key = "sk-9f7010d9001c4e68b3b0f3c39acb560e"
base_url = "https://api.deepseek.com"
client = OpenAI(api_key=api_key, base_url=base_url)

response_settings = {
	"model": "deepseek-chat",
	"stream": False,
	"temperature": 1,
	"frequency_penalty": 1}
