from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from config import TOKEN
from tinydb import TinyDB
from googletrans import Translator

db = TinyDB('uzbek.json')

def introduce(update, context):
    reply = [
        ['uzbek words'],['clear uzbek words'],
         ['🔙 Back to main menu'],
        ]
    key = ReplyKeyboardMarkup(reply)
    update.message.reply_text("Hey, welcome to Uzbek selection! you can find there enlish-uzb transltete words", reply_markup=key)
def clear_uzb(update,context):
    update.message.reply_text('please sen me topic name to delete it exapmle: !topic_name uzb')
def translation(update, context):
    text = update.message.text.strip()
    parts = text.split('*')

    if len(parts) < 2:
        update.message.reply_text("❌ Xatolik: Iltimos, matnni 'word*translation' formatida yuboring.")
        return

    matn = parts[0].strip()
    tarjima = parts[1].strip()

    topic_db = TinyDB(f'{matn}uzb.json')
    translator = Translator()
    result = translator.translate(tarjima, src='en', dest='uz')

    topic_db.insert({'english': tarjima, 'tarjima': result.text})

   
    topics = db.all()
    if matn and matn.strip(): 
         if not any(i.get('topic_name') == matn for i in topics):
               db.insert({'topic_name': matn})
    else:
       update.message.reply_text("❌ Xatolik: Mavzu nomi bo‘sh bo‘lishi mumkin emas!")
    return
    

def show_uzb(update, context):
    if len(db) == 0:
        update.message.reply_text("📂 *Sizning mavzular ro‘yxatingiz bo‘sh.*\n"
                                  "➡️ Yangi mavzu yaratib boshlang! 🎯",
                                  parse_mode="Markdown")
        return

    message = "📖 *Barcha mavzular va so‘zlar:* 📚\n\n"
    topics = db.all()
    
    for topic_entry in topics:
        topic = topic_entry.get("topic_name")  
        topic_db = TinyDB(f"{topic}uzb.json")
        words = topic_db.all()

        message += f"📌 *{topic}* ({len(words)} so‘zlar):\n"

        if words:
            for index, word in enumerate(words, start=1):  
                if 'english' in word and 'tarjima' in word:
                    message += f"   {index}. {word['english']} — {word['tarjima']}\n"
                else:
                    message += f"   ⚠️ Xatolik: {topic}.json ichida noto‘g‘ri ma’lumot formati.\n"
        else:
            message += "   ⚠️ Hozircha hech qanday so‘z qo‘shilmagan.\n"

        message += "\n"

    update.message.reply_text(message, parse_mode="Markdown")
