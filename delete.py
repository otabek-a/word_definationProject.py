from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from config import TOKEN
from defination import get_definition
from topic import topic_name,add_topic,list_topic,matn,show_list
import defination
from tinydb import TinyDB
res = defination.get_topics()
def clear_data(update,context):
    update.message.reply_text('Please if you want delete topic sen me true format example: !topic_name')
def clear_base(update,context):
    global res
    text=update.message.text.strip()
    text=text.replace('!','')
    if text in res:
        db=TinyDB(f'{text}.json')
        db.truncate()
        update.message.reply_text(f'you delete {text} topic')
    else:
         update.message.reply_text(f'you dont have{text} topic')
