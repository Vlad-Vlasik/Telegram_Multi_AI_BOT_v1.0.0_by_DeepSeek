from telegram import Update
from telegram.ext import ContextTypes
from database.models import User, UserSession
from keyboards.menus import get_ai_selection_keyboard

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
    UserSession.get_or_create(user_id=user.id)
    
    await update.message.reply_text(
        "🤖 Вітаю в мульти-AI боті!\n"
        "Оберіть AI для спілкування:",
        reply_markup=get_ai_selection_keyboard()
    )