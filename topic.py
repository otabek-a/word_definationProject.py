from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from tinydb import TinyDB
from config import TOKEN

res = []

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyTelegramBot/1.0 (contact: example@email.com)",
    language="en"
)

def matn(update, context):
    update.message.reply_text("✍️ *Adding words to a topic:* 📝\n\n"
                              "Please send your word in this format:\n"
                              "📌 *Topic_name*️⃣ *your_word*",
                              parse_mode="Markdown")

def list_topic(update, context):
    if not res:
        update.message.reply_text("📂 *Your topic list is empty.*\n"
                                  "➡️ Create a new topic to get started! 🎯",
                                  parse_mode="Markdown")
        return

    message = "📝 *Your Topics:* 📖\n\n"
    for index, topic in enumerate(res, start=1):
        db = TinyDB(f"{topic}.json")  
        word_count = len(db)  
        message += f"{index}. 📌 *{topic}* — {word_count} words 📖\n"

    update.message.reply_text(message, parse_mode="Markdown")

def topic_name(update, context):
    reply = [
        ['➕ Add words to topic', '📜 Show list of topics'],
        ['🔙 Back to main menu']
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("📢 *Enter a topic name*\n\n"
                              "🔹🏫Example: `school/` ",
                              reply_markup=key,
                              parse_mode="Markdown")

def add_topic(update, context):
    global res
    text = update.message.text.strip()
    a = text
    text = text.replace('/', '')

    if text in res:
        update.message.reply_text(f"⚠️ *You already have this topic:* 📌 {a}", parse_mode="Markdown")
        return

    if text:
        db = TinyDB(f"{text}.json")
        res.append(text)
        update.message.reply_text(f"✅ *New topic created:* 📌 {a}", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠️ *Topic cannot be empty!* ❌", parse_mode="Markdown")
