from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import AVAILABLE_AI

def get_ai_selection_keyboard():
    keyboard = []
    for ai_key, ai_name in AVAILABLE_AI.items():
        keyboard.append([InlineKeyboardButton(ai_name, callback_data=f"ai_{ai_key}")])
    return InlineKeyboardMarkup(keyboard)

def get_forward_keyboard(current_ai: str):
    keyboard = []
    for ai_key, ai_name in AVAILABLE_AI.items():
        if ai_key != current_ai:
            keyboard.append([
                InlineKeyboardButton(
                    f"↪️ Переслати до {ai_name}", 
                    callback_data=f"forward_{ai_key}"
                )
            ])
    return InlineKeyboardMarkup(keyboard)