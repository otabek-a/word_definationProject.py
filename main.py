from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from config import TOKEN
from defination import get_definition
from topic import topic_name,add_topic,list_topic,matn,show_list
from delete import clear_base,clear_data
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyTelegramBot/1.0 (contact: example@email.com)",  
    language="en"
)
def check_message(update,context):
    text=update.message.text
    if '!' in text:
        clear_base(update,context)
    if '*' in text:

        get_definition(update,context)
    if text.endswith('/'):
        add_topic(update,context)


def start(update, context):
    reply = [
        ['👨‍🎓 create topic', 'test'],
      
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("👋 Hello! Welcome to defination bot 🤖!\nPlease choose an option to proceed: ⬇️", reply_markup=key)




updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.regex('clear topic'), clear_data))
dispatcher.add_handler(MessageHandler(Filters.regex('show all list'), show_list))
dispatcher.add_handler(MessageHandler(Filters.regex('(?i)^➕ Add words to topic$'), matn))
dispatcher.add_handler(MessageHandler(Filters.regex('(?i)^🔙 Back to main menu$'), start))
dispatcher.add_handler(MessageHandler(Filters.regex('(?i)^📜 Show list of topics$'), list_topic))
dispatcher.add_handler(MessageHandler(Filters.regex('👨‍🎓 create topic'), topic_name))

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, check_message))
# dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_definition))

updater.start_polling()
updater.idle()
