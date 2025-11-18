from .gemini import GeminiProvider
from .chatgpt import ChatGPTProvider
from .deepseek import DeepSeekProvider
from .groq import GroqProvider
from config import GEMINI_API_KEY, OPENAI_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY

class AIProviderFactory:
    @staticmethod
    def create_provider(ai_name: str):
        if ai_name == "gemini":
            return GeminiProvider(GEMINI_API_KEY)
        elif ai_name == "chatgpt":
            return ChatGPTProvider(OPENAI_API_KEY)
        elif ai_name == "deepseek":
            return DeepSeekProvider(DEEPSEEK_API_KEY)
        elif ai_name == "groq":
            return GroqProvider(GROQ_API_KEY)
        else:
            raise ValueError(f"Невідомий AI: {ai_name}")