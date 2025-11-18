from telegram import Update
from telegram.ext import ContextTypes
from database.models import UserSession

async def handle_ai_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    ai_choice = query.data.replace("ai_", "")
    
    # Оновлення сесії в БД
    session = UserSession.get(UserSession.user_id == user_id)
    session.current_ai = ai_choice
    session.save()
    
    await query.edit_message_text(f"✅ Обрано {ai_choice}. Напишіть ваш запит:")