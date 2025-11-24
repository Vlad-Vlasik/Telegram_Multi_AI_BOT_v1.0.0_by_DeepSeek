import os
from dotenv import load_dotenv

load_dotenv()

# Отримуємо змінні оточення з Railway
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# База даних
DATABASE_NAME = os.getenv("DATABASE_URL", "ai_chat_bot.db")

# Динамічно визначаємо доступні AI
def get_available_ai():
    available = {}
    
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
        available["gemini"] = "Google Gemini"
    if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        available["chatgpt"] = "ChatGPT"
    if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your_deepseek_api_key_here":
        available["deepseek"] = "DeepSeek"
    if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
        available["groq"] = "Groq"
    
    return available

AVAILABLE_AI = get_available_ai()

# Логування конфігурації
if __name__ == "__main__":
    print("🔧 Конфігурація Railway:")
    print(f"   TELEGRAM_BOT_TOKEN: {'✅' if TELEGRAM_BOT_TOKEN else '❌'}")
    print(f"   GEMINI_API_KEY: {'✅' if GEMINI_API_KEY else '❌'}")
    print(f"   OPENAI_API_KEY: {'✅' if OPENAI_API_KEY else '❌'}")
    print(f"   DEEPSEEK_API_KEY: {'✅' if DEEPSEEK_API_KEY else '❌'}")
    print(f"   GROQ_API_KEY: {'✅' if GROQ_API_KEY else '❌'}")
    print(f"   Доступні AI: {', '.join(AVAILABLE_AI.values()) or 'жоден'}")
