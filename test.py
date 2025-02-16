from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
def test_data(update,tontext):
    key=[['result of test'], ['🔙 Back to main menu'],]
    reply_key=ReplyKeyboardMarkup(key)
    update.message.reply_text('Hey please if you want to start quiz please send me true format example: topic_name?',reply_markup=reply_key)
