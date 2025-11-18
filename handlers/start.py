from telegram import Update
from telegram.ext import ContextTypes
from database.models import User, UserSession
from keyboards.menus import get_ai_selection_keyboard
from config import AVAILABLE_AI

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Збереження користувача в БД
    User.get_or_create(
        user_id=user.id,
        defaults={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    )
    
    # Створення сесії
    session, created = UserSession.get_or_create(
        user_id=user.id,
        defaults={'current_ai': list(AVAILABLE_AI.keys())[0] if AVAILABLE_AI else 'gemini'}
    )
    
    if not AVAILABLE_AI:
        await update.message.reply_text(
            "❌ Жоден AI не налаштований. Будь ласка, додайте хоча б один API ключ у файлі .env"
        )
        return
    
    await update.message.reply_text(
        "🤖 Вітаю в мульти-AI боті!\n"
        f"Доступні AI: {', '.join(AVAILABLE_AI.values())}\n"
        "Оберіть AI для спілкування:",
        reply_markup=get_ai_selection_keyboard()
    )