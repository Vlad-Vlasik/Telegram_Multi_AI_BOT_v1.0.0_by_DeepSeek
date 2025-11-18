from groq import Groq
from .base import BaseAIProvider

class GroqProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "groq"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama2-70b-4096",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка Groq: {str(e)}"