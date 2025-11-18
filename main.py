import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from database.models import create_tables
from handlers.start import start
from handlers.ai_selection import handle_ai_selection
from handlers.message import handle_message, handle_forwarding

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Ініціалізація бази даних
    create_tables()
    
    # Створення додатку
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Додавання обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_ai_selection, pattern="^ai_"))
    application.add_handler(CallbackQueryHandler(handle_forwarding, pattern="^forward_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()