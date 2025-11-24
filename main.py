#!/usr/bin/env python3
"""
Telegram Multi-AI Bot для Railway
"""

import os
import sys
import logging

# Додаємо поточну директорію до Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Налаштування логування для Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Налаштовує середовище та перевіряє залежності"""
    print("🔧 Налаштування середовища Railway...")
    
    # Перевірка та імпорт залежностей
    dependencies = [
        ('telegram.ext', 'python-telegram-bot'),
        ('google.generativeai', 'google-generativeai'),
        ('openai', 'openai'),
        ('dotenv', 'python-dotenv'),
        ('peewee', 'peewee'),
        ('groq', 'groq')
    ]
    
    missing_deps = []
    for module, package in dependencies:
        try:
            __import__(module.split('.')[0])
            print(f"✅ {package} завантажено")
        except ImportError as e:
            missing_deps.append(package)
            print(f"❌ {package} відсутній: {e}")
    
    if missing_deps:
        logger.error(f"Відсутні залежності: {', '.join(missing_deps)}")
        return False
    
    return True

def import_project_modules():
    """Імпортує модулі проекту"""
    try:
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
        from config import TELEGRAM_BOT_TOKEN, AVAILABLE_AI
        from database.models import create_tables
        from handlers.start import start
        from handlers.ai_selection import handle_ai_selection
        from handlers.message import handle_message, handle_forwarding
        from ai_providers import AIProviderFactory
        
        print("✅ Всі модулі проекту завантажено")
        return TELEGRAM_BOT_TOKEN, AVAILABLE_AI
    except ImportError as e:
        logger.error(f"Помилка імпорту модулів проекту: {e}")
        return None, None

def main():
    """Основна функція запуску"""
    print("=" * 60)
    print("🚂 Запуск на Railway")
    print("🤖 Telegram Multi-AI Bot")
    print("=" * 60)
    
    # Налаштування середовища
    if not setup_environment():
        sys.exit(1)
    
    # Імпорт модулів проекту
    TELEGRAM_BOT_TOKEN, AVAILABLE_AI = import_project_modules()
    if not TELEGRAM_BOT_TOKEN:
        sys.exit(1)
    
    # Перевірка токена
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error("TELEGRAM_BOT_TOKEN не налаштовано")
        print("\n🔧 Налаштуйте змінні оточення в Railway:")
        print("   TELEGRAM_BOT_TOKEN=ваш_токен_бота")
        print("   GEMINI_API_KEY=ваш_ключ_gemini")
        print("   OPENAI_API_KEY=ваш_ключ_openai")
        print("   DEEPSEEK_API_KEY=ваш_ключ_deepseek")
        print("   GROQ_API_KEY=ваш_ключ_groq")
        sys.exit(1)
    
    # Ініціалізація бази даних
    try:
        create_tables()
        logger.info("База даних ініціалізована")
    except Exception as e:
        logger.error(f"Помилка ініціалізації БД: {e}")
        # Продовжуємо, оскільки бот може працювати без БД
    
    # Запуск бота
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Додавання обробників
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_ai_selection, pattern="^ai_"))
        application.add_handler(CallbackQueryHandler(handle_forwarding, pattern="^forward_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("\n" + "=" * 50)
        print("✅ Бот успішно запущений на Railway!")
        print("📍 Використовуйте /start в Telegram")
        print("📊 Доступні AI:", ", ".join(AVAILABLE_AI.values()) if AVAILABLE_AI else "жоден")
        print("=" * 50 + "\n")
        
        # Запуск полінгу
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        
    except Exception as e:
        logger.error(f"Помилка запуску бота: {e}")
        print(f"💡 Можливі причини: {e}")

if __name__ == "__main__":
    main()
