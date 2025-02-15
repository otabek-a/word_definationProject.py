from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from tinydb import TinyDB, Query
from config import TOKEN
import defination

# Topics bazasini yaratamiz
res = TinyDB("topics.json")

def show_list(update, context):
    global res

    if len(res) == 0:
        update.message.reply_text("📂 *Your topic list is empty.*\n"
                                  "➡️ Create a new topic to get started! 🎯",
                                  parse_mode="Markdown")
        return

    message = "📖 *All Topics and Words:* 📚\n\n"
    topics = res.all()
    
    for topic_entry in topics:
        topic = topic_entry.get("name")  # Bazadan topic nomini olamiz
        db = TinyDB(f"{topic}.json")
        words = db.all()

        message += f"📌 *{topic}* ({len(words)} words):\n"

        if words:
            for index, word in enumerate(words, start=1):  
                if 'term' in word and 'definition' in word:
                    message += f"   {index}. {word['term']} — {word['definition']}\n"
                else:
                    message += f"   ⚠️ Error: Invalid data format in {topic}.json\n"
        else:
            message += "   ⚠️ No words added yet.\n"

        message += "\n"

    update.message.reply_text(message, parse_mode="Markdown")

def matn(update, context):
    update.message.reply_text("✍️ *Adding words to a topic:* 📝\n\n"
                              "Please send your word in this format:\n"
                              "📌 Topic_name*your_word",
                              )

def list_topic(update, context):
    if len(res) == 0:
        update.message.reply_text("📂 *Your topic list is empty.*\n"
                                  "➡️ Create a new topic to get started! 🎯",
                                  parse_mode="Markdown")
        return

    message = "📝 *Your Topics:* 📖\n\n"
    for index, topic_entry in enumerate(res.all(), start=1):
        topic = topic_entry.get("name")  
        db = TinyDB(f"{topic}.json")  
        word_count = len(db)  
        message += f"{index}. 📌 *{topic}* — {word_count} words 📖\n"

    update.message.reply_text(message, parse_mode="Markdown")

def topic_name(update, context):
    reply = [
        ['show all list'],
        ['➕ Add words to topic', '📜 Show list of topics'],
        ['🔙 Back to main menu'],
        ['clear topic']
    ]
    key = ReplyKeyboardMarkup(reply, resize_keyboard=True)
    update.message.reply_text("📢 *Enter a topic name*\n\n"
                              "🔹🏫Example: school/ ",
                              reply_markup=key,
                              parse_mode="Markdown")

def add_topic(update, context):
    global res
    text = update.message.text.strip().lower()
    text = text.replace('/', '')

    # TinyDB dan mavzuni qidiramiz
    Topic = Query()
    existing_topic = res.search(Topic.name == text)

    if existing_topic:
        update.message.reply_text(f"⚠️ *You already have this topic:* 📌 {text}", parse_mode="Markdown")
        return

    if text:
        res.insert({"name": text})  # TinyDB ga yangi mavzuni kiritamiz
        TinyDB(f"{text}.json")  # Mavzu uchun alohida fayl yaratamiz
        update.message.reply_text(f"✅ *New topic created:* 📌 {text}", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠️ *Topic cannot be empty!* ❌", parse_mode="Markdown")
