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

# Available AI Models
AVAILABLE_AI = {
    "gemini": "Google Gemini",
    "chatgpt": "ChatGPT", 
    "deepseek": "DeepSeek",
    "groq": "Groq"
}