import os
import zipfile

def create_project_structure():
    """Створює точну структуру проекту Telegram AI Bot"""
    
    base_dir = "telegram-ai-bot"
    
    # Створення директорій
    directories = [
        base_dir,
        f"{base_dir}/database",
        f"{base_dir}/ai_providers",
        f"{base_dir}/handlers", 
        f"{base_dir}/keyboards"
    ]
    
    print("📁 Створення структури директорій...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}/")
    
    # Створення файлів
    files = {
        # Основні файли
        f"{base_dir}/main.py": "",
        f"{base_dir}/config.py": "",
        f"{base_dir}/requirements.txt": "",
        
        # Database
        f"{base_dir}/database/__init__.py": "",
        f"{base_dir}/database/models.py": "",
        
        # AI Providers
        f"{base_dir}/ai_providers/__init__.py": "",
        f"{base_dir}/ai_providers/base.py": "",
        f"{base_dir}/ai_providers/gemini.py": "",
        f"{base_dir}/ai_providers/chatgpt.py": "",
        f"{base_dir}/ai_providers/deepseek.py": "",
        f"{base_dir}/ai_providers/groq.py": "",
        
        # Handlers
        f"{base_dir}/handlers/__init__.py": "",
        f"{base_dir}/handlers/start.py": "",
        f"{base_dir}/handlers/ai_selection.py": "",
        f"{base_dir}/handlers/message.py": "",
        
        # Keyboards
        f"{base_dir}/keyboards/__init__.py": "",
        f"{base_dir}/keyboards/menus.py": "",
    }
    
    print("\\n📄 Створення файлів...")
    for file_path, content in files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {file_path}")
    
    # Заповнення файлів основним кодом
    print("\\n🔄 Заповнення файлів кодом...")
    fill_files_with_content(base_dir)
    
    # Створення ZIP архіву
    create_zip_archive(base_dir)
    
    print(f"\\n🎉 Проект успішно створено!")
    print(f"📦 ZIP архів: {base_dir}.zip")
    print(f"📁 Основна тека: {base_dir}/")
    print(f"\\n📋 Структура проекту:")
    print_project_structure(base_dir)

def fill_files_with_content(base_dir):
    """Заповнює файли основним кодом"""
    
    # main.py
    main_py_content = '''import logging
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
    print("🤖 Бот запускається...")
    application.run_polling()

if __name__ == "__main__":
    main()
'''
    write_file(f"{base_dir}/main.py", main_py_content)
    
    # config.py
    config_py_content = '''import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# AI API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Database
DATABASE_NAME = "ai_chat_bot.db"

# Динамічно визначаємо доступні AI на основі наявних API ключів
def get_available_ai():
    available = {}
    
    if GEMINI_API_KEY:
        available["gemini"] = "Google Gemini"
    if OPENAI_API_KEY:
        available["chatgpt"] = "ChatGPT"
    if DEEPSEEK_API_KEY:
        available["deepseek"] = "DeepSeek"
    if GROQ_API_KEY:
        available["groq"] = "Groq"
    
    return available

AVAILABLE_AI = get_available_ai()
'''
    write_file(f"{base_dir}/config.py", config_py_content)
    
    # requirements.txt
    requirements_content = '''python-telegram-bot==20.7
google-generativeai>=0.3.0
openai>=1.0.0
python-dotenv>=1.0.0
peewee>=3.17.0
groq>=0.3.0
'''
    write_file(f"{base_dir}/requirements.txt", requirements_content)
    
    # database/models.py
    models_content = '''from peewee import *
import datetime

db = SqliteDatabase('ai_chat_bot.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = BigIntegerField(unique=True)
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)

class Conversation(BaseModel):
    user = ForeignKeyField(User, backref='conversations')
    ai_model = CharField()
    user_message = TextField()
    ai_response = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

class UserSession(BaseModel):
    user = ForeignKeyField(User, backref='sessions', unique=True)
    current_ai = CharField(default='gemini')
    last_question = TextField(null=True)
    last_response = TextField(null=True)
    updated_at = DateTimeField(default=datetime.datetime.now)

def create_tables():
    db.connect()
    db.create_tables([User, Conversation, UserSession], safe=True)
    db.close()
'''
    write_file(f"{base_dir}/database/models.py", models_content)
    
    # ai_providers/__init__.py
    ai_providers_init_content = '''from .gemini import GeminiProvider
from .chatgpt import ChatGPTProvider
from .deepseek import DeepSeekProvider
from .groq import GroqProvider
from config import GEMINI_API_KEY, OPENAI_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY

class AIProviderFactory:
    @staticmethod
    def create_provider(ai_name: str):
        try:
            if ai_name == "gemini" and GEMINI_API_KEY:
                return GeminiProvider(GEMINI_API_KEY)
            elif ai_name == "chatgpt" and OPENAI_API_KEY:
                return ChatGPTProvider(OPENAI_API_KEY)
            elif ai_name == "deepseek" and DEEPSEEK_API_KEY:
                return DeepSeekProvider(DEEPSEEK_API_KEY)
            elif ai_name == "groq" and GROQ_API_KEY:
                return GroqProvider(GROQ_API_KEY)
            else:
                return None
        except Exception as e:
            print(f"Помилка створення провайдера {ai_name}: {e}")
            return None
    
    @staticmethod
    def is_provider_available(ai_name: str) -> bool:
        if ai_name == "gemini":
            return bool(GEMINI_API_KEY)
        elif ai_name == "chatgpt":
            return bool(OPENAI_API_KEY)
        elif ai_name == "deepseek":
            return bool(DEEPSEEK_API_KEY)
        elif ai_name == "groq":
            return bool(GROQ_API_KEY)
        return False
'''
    write_file(f"{base_dir}/ai_providers/__init__.py", ai_providers_init_content)
    
    # ai_providers/base.py
    base_content = '''from abc import ABC, abstractmethod

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
'''
    write_file(f"{base_dir}/ai_providers/base.py", base_content)
    
    # ai_providers/gemini.py
    gemini_content = '''import google.generativeai as genai
from .base import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    @property
    def name(self) -> str:
        return "gemini"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Помилка Gemini: {str(e)}"
'''
    write_file(f"{base_dir}/ai_providers/gemini.py", gemini_content)
    
    # ai_providers/chatgpt.py
    chatgpt_content = '''from openai import OpenAI
from .base import BaseAIProvider

class ChatGPTProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "chatgpt"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка ChatGPT: {str(e)}"
'''
    write_file(f"{base_dir}/ai_providers/chatgpt.py", chatgpt_content)
    
    # ai_providers/deepseek.py
    deepseek_content = '''from openai import OpenAI
from .base import BaseAIProvider

class DeepSeekProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
    
    @property
    def name(self) -> str:
        return "deepseek"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка DeepSeek: {str(e)}"
'''
    write_file(f"{base_dir}/ai_providers/deepseek.py", deepseek_content)
    
    # ai_providers/groq.py
    groq_content = '''from groq import Groq
from .base import BaseAIProvider

class GroqProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "groq"
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama2-70b-4096",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка Groq: {str(e)}"
'''
    write_file(f"{base_dir}/ai_providers/groq.py", groq_content)
    
    # handlers/start.py
    start_content = '''from telegram import Update
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
        "🤖 Вітаю в мульти-AI боті!\\n"
        f"Доступні AI: {', '.join(AVAILABLE_AI.values())}\\n"
        "Оберіть AI для спілкування:",
        reply_markup=get_ai_selection_keyboard()
    )
'''
    write_file(f"{base_dir}/handlers/start.py", start_content)
    
    # handlers/ai_selection.py
    ai_selection_content = '''from telegram import Update
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
'''
    write_file(f"{base_dir}/handlers/ai_selection.py", ai_selection_content)
    
    # handlers/message.py
    message_content = '''from telegram import Update
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
            f"🤖 **Відповідь від {ai_service}:**\\n\\n{response}",
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
            f"'{session.last_question}':\\n\\n{session.last_response}\\n\\n"
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
            f"🔁 **Переслано до {target_ai}:**\\n\\n{new_response}",
            reply_markup=get_forward_keyboard(target_ai)
        )
        
    except Exception as e:
        await query.message.reply_text(f"❌ Помилка пересилання: {str(e)}")
'''
    write_file(f"{base_dir}/handlers/message.py", message_content)
    
    # keyboards/menus.py
    menus_content = '''from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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
'''
    write_file(f"{base_dir}/keyboards/menus.py", menus_content)

def write_file(file_path, content):
    """Записує вміст у файл"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_zip_archive(base_dir):
    """Створює ZIP архів проекту"""
    zip_filename = f"{base_dir}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=base_dir + "/..")
                zipf.write(file_path, arcname)
    
    print(f"  ✅ Створено ZIP архів: {zip_filename}")

def print_project_structure(base_dir):
    """Виводить структуру проекту у вигляді дерева"""
    for root, dirs, files in os.walk(base_dir):
        level = root.replace(base_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}├── {os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}├── {file}')

if __name__ == "__main__":
    create_project_structure()