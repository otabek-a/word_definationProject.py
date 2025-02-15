from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from tinydb import TinyDB,Query
from config import TOKEN
from tinydb import where
result = TinyDB("topics.json")


wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyTelegramBot/1.0 (contact: example@email.com)",  # O'zingizning User-Agent
    language="en"
)


def get_definition(update, context):
    text = update.message.text.strip()
    parts = text.split('*')
    global result
    if len(parts) < 2:
        update.message.reply_text("⚠️ Please use the correct format: *Topic_name*word*")
        return

    topic = parts[0].strip()
    word = parts[1].strip()

    page = wiki_wiki.page(word)

    if not page.exists():
        update.message.reply_text(f"❌ Sorry, no definition found for '{word}'.")
        return

    summary = page.summary
    sentences = summary.split('. ')
    short_definition = '. '.join(sentences[:1])
    clean_definition = short_definition.replace(word, "This term").replace(word.capitalize(), "This term")

    db = TinyDB(f"{topic}.json")
    
    Word = Query()

    if db.search(Word.term == word):
        update.message.reply_text(f"📌 '{word}' is already in the database.")
    else:
        db.insert({"term": word, "definition": clean_definition})
        update.message.reply_text(f"✅ '{word}' has been added to *{topic}* database.")
    if not result.search(where('topic_name') == topic):
       result.insert({'topic_name': topic})
def get_topics():
    return result