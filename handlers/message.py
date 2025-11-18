from telegram import Update
from telegram.ext import ContextTypes
from database.models import UserSession, Conversation
from ai_providers import AIProviderFactory
from keyboards.menus import get_forward_keyboard

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    try:
        # Отримання сесії з БД
        session = UserSession.get(UserSession.user_id == user_id)
        ai_service = session.current_ai
        
        # Перевірка чи доступний обраний AI
        if not AIProviderFactory.is_provider_available(ai_service):
            await update.message.reply_text(
                f"❌ {ai_service} наразі недоступний. Будь ласка, оберіть інший AI через /start"
            )
            return
        
        # Генерація відповіді через обраний AI
        provider = AIProviderFactory.create_provider(ai_service)
        if provider is None:
            await update.message.reply_text(
                f"❌ Помилка ініціалізації {ai_service}. Спробуйте інший AI."
            )
            return
            
        response = await provider.generate_response(user_message)
        
        # Збереження розмови в БД
        Conversation.create(
            user_id=user_id,
            ai_model=ai_service,
            user_message=user_message,
            ai_response=response
        )
        
        # Оновлення сесії
        session.last_question = user_message
        session.last_response = response
        session.save()
        
        # Відправка відповіді з кнопкою пересилання
        await update.message.reply_text(
            f"🤖 **Відповідь від {ai_service}:**\n\n{response}",
            reply_markup=get_forward_keyboard(ai_service)
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка: {str(e)}")

async def handle_forwarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    target_ai = query.data.replace("forward_", "")
    
    try:
        # Перевірка чи доступний цільовий AI
        if not AIProviderFactory.is_provider_available(target_ai):
            await query.answer(f"❌ {target_ai} недоступний для пересилання")
            return
        
        # Отримання сесії з БД
        session = UserSession.get(UserSession.user_id == user_id)
        
        if not session.last_question or not session.last_response:
            await query.answer("Немає попереднього повідомлення для пересилання")
            return
        
        # Формування нового запиту
        prompt = (
            f"Попередня відповідь від {session.current_ai} на запит: "
            f"'{session.last_question}':\n\n{session.last_response}\n\n"
            f"Проаналізуй цю відповідь та дай свої коментарі:"
        )
        
        # Генерація відповіді через новий AI
        provider = AIProviderFactory.create_provider(target_ai)
        if provider is None:
            await query.message.reply_text(f"❌ Помилка ініціалізації {target_ai}")
            return
            
        new_response = await provider.generate_response(prompt)
        
        # Збереження нової розмови в БД
        Conversation.create(
            user_id=user_id,
            ai_model=target_ai,
            user_message=prompt,
            ai_response=new_response
        )
        
        # Оновлення сесії
        session.current_ai = target_ai
        session.last_question = prompt
        session.last_response = new_response
        session.save()
        
        # Відправка відповіді
        await query.message.reply_text(
            f"🔁 **Переслано до {target_ai}:**\n\n{new_response}",
            reply_markup=get_forward_keyboard(target_ai)
        )
        
    except Exception as e:
        await query.message.reply_text(f"❌ Помилка пересилання: {str(e)}")