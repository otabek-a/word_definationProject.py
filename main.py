from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from tinydb import TinyDB
from telegram import ReplyKeyboardMarkup
from config import TOKEN
from defination import get_definition
from topic import topic_name,add_topic,list_topic,matn,show_list,new_topic
from delete import clear_base,clear_data
from uzbek_data import introduce,translation,show_uzb,clear_uzb
from test import test_data,quiz_test,ask_question,get_answer,javob_chiqar
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyTelegramBot/1.0 (contact: example@email.com)",  
    language="en"
)
j=TinyDB('total.json')
def check_message(update,context):
    global j
    text=update.message.text.lower()
    if text=='begin':
        j.truncate()
        ask_question(update,context)
    if text.endswith('?'):
        quiz_test(update,context)
    
    if '!' in text:
        clear_base(update,context)
    if '*' in text:
        new_topic(update,context)
        get_definition(update,context)
        translation(update,context)
    if text.endswith('/'):
        add_topic(update,context)
    if '?' not in text and '/' not in text and text!='begin' and '!' not in text and '*' not in text:
        get_answer(update,context)


def start(update, context):
    reply = [
        ['👨‍🎓 create topic', 'test'],
        ['uzbek section'],
      
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("👋 Hello! Welcome to defination bot 🤖!\nPlease choose an option to proceed: ⬇️", reply_markup=key)




updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.regex('result of test'),javob_chiqar))
dispatcher.add_handler(MessageHandler(Filters.regex('test'),test_data))
dispatcher.add_handler(MessageHandler(Filters.regex('clear uzbek words'),clear_uzb))
dispatcher.add_handler(MessageHandler(Filters.regex('uzbek words'), show_uzb))
dispatcher.add_handler(MessageHandler(Filters.regex('uzbek section'), introduce))
dispatcher.add_handler(MessageHandler(Filters.regex('clear topic'), clear_data))
dispatcher.add_handler(MessageHandler(Filters.regex('show all list'), show_list))
dispatcher.add_handler(MessageHandler(Filters.regex('(?i)^➕ Add words to topic$'), matn))
dispatcher.add_handler(MessageHandler(Filters.regex('(?i)^🔙 Back to main menu$'), start))
dispatcher.add_handler(MessageHandler(Filters.regex('(?i)^📜 Show list of topics$'), list_topic))
dispatcher.add_handler(MessageHandler(Filters.regex('👨‍🎓 create topic'), topic_name))

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, check_message))



updater.start_polling()
updater.idle()
