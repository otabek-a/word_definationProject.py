from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from tinydb import TinyDB
import time

res = TinyDB("topics.json")
text = ''
result=TinyDB('javob.json')
def test_data(update, context):
    key = [['result of test'], ['🔙 Back to main menu']]
    reply_key = ReplyKeyboardMarkup(key, one_time_keyboard=True)
    update.message.reply_text(
        'Hey, please send the topic name in the correct format (e.g., topic_name?).',
        reply_markup=reply_key
    )

def quiz_test(update, context):
    global text
    matn = update.message.text.replace('?', '').strip().lower()
    text = matn
    count = any(i.get('topic_name') == matn for i in res.all())

    if count:
        update.message.reply_text(f'We started the topic "{matn}". If you are ready, send "begin".')
    else:
        update.message.reply_text(f'I cannot find the topic "{matn}".')

def ask_question(update, context):
    global text
    db = TinyDB(f'{text}.json')
    records = db.all()
    
    index = 0
    
    
    while index < len(records):
        update.message.reply_text(f'{index+1} topic: {text} Question: {records[index].get("definition")}')
        
        user_input=update.message.text
        
        if user_input.lower() == 'exit':
            update.message.reply_text("Quiz finished.")
            break
        time.sleep(10)
        index+=1

def get_answer(update,context):
    global result
    matn=update.message.text
    result.insert({'answer':matn})
    print(result.all())



