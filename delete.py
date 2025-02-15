from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from config import TOKEN
from defination import get_definition
from topic import topic_name, add_topic, list_topic, matn, show_list
import defination
from tinydb import TinyDB, where

result = TinyDB("topics.json")
res = result.all()

def clear_data(update, context):
    update.message.reply_text('⚠️ Please, if you want to delete a topic, send me the correct format. Example: !topic_name')

def clear_base(update, context):
    global res
    
    text = update.message.text.replace('!', '').lower().replace(' ', '')
    db = TinyDB(f'{text}.json')
    found = ''
    
    for i in res:
        if i.get('topic_name', '').lower().replace(' ', '') == text or i.get('name', '').lower().replace(' ', ''):
            found = text
    
    if found != '':
        update.message.reply_text(f'✅ You deleted the {text} topic 🗑️')
    else:
        update.message.reply_text(f'❌ You cannot find the {text} topic 🔍')