from .gemini import GeminiProvider
from .chatgpt import ChatGPTProvider
from .deepseek import DeepSeekProvider
from .groq import GroqProvider
from config import GEMINI_API_KEY, OPENAI_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY

class AIProviderFactory:
    @staticmethod
    def create_provider(ai_name: str):
        try:
            if ai_name == "gemini" and GEMINI_API_KEY:
                return GeminiProvider(GEMINI_API_KEY)
            elif ai_name == "chatgpt" and OPENAI_API_KEY:
                return ChatGPTProvider(OPENAI_API_KEY)
            elif ai_name == "deepseek" and DEEPSEEK_API_KEY:
                return DeepSeekProvider(DEEPSEEK_API_KEY)
            elif ai_name == "groq" and GROQ_API_KEY:
                return GroqProvider(GROQ_API_KEY)
            else:
                return None
        except Exception as e:
            print(f"Помилка створення провайдера {ai_name}: {e}")
            return None
    
    @staticmethod
    def is_provider_available(ai_name: str) -> bool:
        if ai_name == "gemini":
            return bool(GEMINI_API_KEY)
        elif ai_name == "chatgpt":
            return bool(OPENAI_API_KEY)
        elif ai_name == "deepseek":
            return bool(DEEPSEEK_API_KEY)
        elif ai_name == "groq":
            return bool(GROQ_API_KEY)
        return False