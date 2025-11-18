import logging
import os
import sys
import subprocess

def check_dependencies():
    """Перевіряє та встановлює необхідні бібліотеки"""
    required_packages = {
        'python-telegram-bot': 'telegram',
        'google-generativeai': 'google.generativeai',
        'openai': 'openai',
        'python-dotenv': 'dotenv',
        'peewee': 'peewee',
        'groq': 'groq',
        'requests': 'requests'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            if import_name == 'telegram':
                from telegram import __version__
            else:
                __import__(import_name)
            print(f"✅ {package} встановлено")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} відсутній")
    
    return missing_packages

def install_packages(packages):
    """Встановлює відсутні пакети"""
    if not packages:
        return True
        
    print(f"\n📦 Встановлення відсутніх пакетів: {', '.join(packages)}")
    try:
        for package in packages:
            if package == 'python-telegram-bot':
                subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} успішно встановлено")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка встановлення {package}: {e}")
        return False

def main():
    """Основна функція з автоматичною установкою залежностей"""
    print("🔍 Перевірка залежностей...")
    
    # Перевірка та встановлення відсутніх пакетів
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"\n⚠️  Відсутні {len(missing_packages)} пакетів")
        if not install_packages(missing_packages):
            print("\n❌ Не вдалося встановити всі залежності")
            print("💡 Спробуйте встановити вручну:")
            print("   pip install python-telegram-bot==20.7 google-generativeai openai python-dotenv peewee groq requests")
            return
    
    # Тепер імпортуємо всі модулі
    try:
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
        from config import TELEGRAM_BOT_TOKEN, AVAILABLE_AI
        from database.models import create_tables
        from handlers.start import start
        from handlers.ai_selection import handle_ai_selection
        from handlers.message import handle_message, handle_forwarding
        from ai_providers import AIProviderFactory
        
        print("✅ Всі залежності завантажено успішно!")
        
    except ImportError as e:
        print(f"❌ Помилка імпорту після встановлення: {e}")
        return

    # Додаємо поточну директорію до Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

    # Налаштування логування
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Перевірка токена бота
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("\n❌ TELEGRAM_BOT_TOKEN не налаштовано!")
        print("📝 Створіть файл .env у корені проекту з вмістом:")
        print("TELEGRAM_BOT_TOKEN=ваш_токен_бота")
        print("\n🔧 Отримайте токен від @BotFather в Telegram")
        return

    # Ініціалізація бази даних
    try:
        create_tables()
        print("✅ База даних ініціалізована")
    except Exception as e:
        print(f"❌ Помилка ініціалізації БД: {e}")
        return

    # Запуск бота
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Додавання обробників
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(handle_ai_selection, pattern="^ai_"))
        application.add_handler(CallbackQueryHandler(handle_forwarding, pattern="^forward_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("\n" + "="*50)
        print("🤖 Бот успішно запущений!")
        print("📍 Використовуйте /start в Telegram")
        print("🛑 Для зупинки натисніть Ctrl+C")
        print("="*50)
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Помилка запуску бота: {e}")

if __name__ == "__main__":
    main()