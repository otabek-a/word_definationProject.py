from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from config import TOKEN


wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyTelegramBot/1.0 (contact: example@email.com)",  # O'zingizning User-Agent
    language="en"
)


def get_definition(update, context):
    word = update.message.text.strip()
    page = wiki_wiki.page(word)

    if not page.exists():
        update.message.reply_text(f"Sorry, no definition found for '{word}'.")
        return

   
    summary = page.summary

   
    sentences = summary.split('. ')  # Jumlalarga ajratish
    short_definition = '. '.join(sentences[:1])  # 3 ta gap olish

   
    clean_definition = short_definition.replace(word, "This term ").replace(word.capitalize(), "This term ")

    update.message.reply_text(f"{word.capitalize()} - {clean_definition}")