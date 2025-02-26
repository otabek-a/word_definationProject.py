from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from tinydb import TinyDB,Query
from config import TOKEN
from tinydb import where
result = TinyDB("topics.json")


wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyTelegramBot/1.0 (contact: example@email.com)", 
    language="en"
)


def get_definition(update, context):
    text = update.message.text.strip()
    parts = text.split('*')
    global result

    if len(parts) < 2 or not parts[0].strip(): 
        update.message.reply_text("⚠️ Please use the correct format: *Topic_name*word*")
        return

    topic = parts[0].strip().lower()
    word = parts[1].strip().lower()
    if not result.search(where('topic_name') == topic):
       update.message.reply_text(f'I cannot find that {topic} please create with {topic}/')
       return
    if  result.search(where('topic_name') == topic):
      page = wiki_wiki.page(word)
    
      if not page.exists():
        update.message.reply_text(f"❌ Sorry, no definition found for '{word}'.")
        return

      summary = page.summary
      sentences = summary.split('. ')
      short_definition = '. '.join(sentences[:1])
      clean_definition = short_definition.replace(word, "This term").replace(word.capitalize(), "This term")

      db = TinyDB(f"{topic}.json")
      salom=False
      Word = Query()
      matn=result.all()
      if db.search(Word.term == word):
          update.message.reply_text(f"📌 '{word}' is already in the database.")
      else:
        db.insert({"term": word, "definition": clean_definition})
        update.message.reply_text(f"✅ '{word}' has been added to *{topic}* database.")
   

      

   



def get_topics():
    return result