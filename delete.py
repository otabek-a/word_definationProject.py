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
    if 'uzb'in text:
       db = TinyDB(f'{text}.json')
       matn=TinyDB('uzbek.json')
       found = ''
       count=False
       for i in matn:
        if i.get('topic_name', '').lower().replace(' ', '') == text :
            found = text
            count=True

       print(db.all())
       db.truncate()
       salom=db.all()
       print(salom)
       if salom==[]:
        
          update.message.reply_text(f'✅ You deleted the {text} topic 🗑️')
       else:
         update.message.reply_text(f'❌ i cannot find the {text} topic 🔍')
       return

    db = TinyDB(f'{text}.json')
    found = ''
    
    for i in res:
        if i.get('topic_name', '').lower().replace(' ', '') == text or i.get('name', '').lower().replace(' ', ''):
            found = text
    db.truncate()
    if found != '':

        update.message.reply_text(f'✅ You deleted the {text} topic 🗑️')
    else:
        update.message.reply_text(f'❌ i cannot find the {text} topic 🔍')