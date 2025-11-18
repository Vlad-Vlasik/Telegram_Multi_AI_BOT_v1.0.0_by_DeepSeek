from peewee import *
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