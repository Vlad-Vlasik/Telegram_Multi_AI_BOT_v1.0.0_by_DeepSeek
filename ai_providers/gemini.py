import google.generativeai as genai
from .base import BaseAIProvider
import os

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    @property
    def name(self) -> str:
        return "gemini"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Помилка Gemini: {str(e)}"