import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# AI API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Database
DATABASE_NAME = "ai_chat_bot.db"

# Динамічно визначаємо доступні AI на основі наявних API ключів
def get_available_ai():
    available = {}
    
    if GEMINI_API_KEY:
        available["gemini"] = "Google Gemini"
    if OPENAI_API_KEY:
        available["chatgpt"] = "ChatGPT"
    if DEEPSEEK_API_KEY:
        available["deepseek"] = "DeepSeek"
    if GROQ_API_KEY:
        available["groq"] = "Groq"
    
    return available

AVAILABLE_AI = get_available_ai()