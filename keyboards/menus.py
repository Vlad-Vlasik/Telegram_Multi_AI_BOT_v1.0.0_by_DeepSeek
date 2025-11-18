from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import AVAILABLE_AI
from ai_providers import AIProviderFactory

def get_ai_selection_keyboard():
    keyboard = []
    for ai_key, ai_name in AVAILABLE_AI.items():
        # Показуємо тільки доступні AI
        if AIProviderFactory.is_provider_available(ai_key):
            keyboard.append([InlineKeyboardButton(ai_name, callback_data=f"ai_{ai_key}")])
    
    # Якщо немає доступних AI
    if not keyboard:
        keyboard.append([InlineKeyboardButton("❌ Немає доступних AI", callback_data="none")])
    
    return InlineKeyboardMarkup(keyboard)

def get_forward_keyboard(current_ai: str):
    keyboard = []
    for ai_key, ai_name in AVAILABLE_AI.items():
        if ai_key != current_ai and AIProviderFactory.is_provider_available(ai_key):
            keyboard.append([
                InlineKeyboardButton(
                    f"↪️ Переслати до {ai_name}", 
                    callback_data=f"forward_{ai_key}"
                )
            ])
    
    # Якщо немає інших доступних AI для пересилання
    if not keyboard:
        keyboard.append([
            InlineKeyboardButton("❌ Немає інших AI для пересилання", callback_data="none")
        ])
    
    return InlineKeyboardMarkup(keyboard)