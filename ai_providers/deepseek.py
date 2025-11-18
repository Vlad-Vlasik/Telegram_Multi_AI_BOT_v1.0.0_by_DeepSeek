from openai import OpenAI
from .base import BaseAIProvider

class DeepSeekProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
    
    @property
    def name(self) -> str:
        return "deepseek"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка DeepSeek: {str(e)}"