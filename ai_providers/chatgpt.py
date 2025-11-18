from openai import OpenAI
from .base import BaseAIProvider

class ChatGPTProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "chatgpt"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка ChatGPT: {str(e)}"