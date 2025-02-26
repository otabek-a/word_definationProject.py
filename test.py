from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from tinydb import TinyDB
import time

res = TinyDB("topics.json")
text = ''
result = TinyDB('javob.json')
j = TinyDB('total.json')
savol = TinyDB('umumiy.json')
true_count = 0
false_count = 0

def test_data(update, context):
    global true_count,false_count
    true_count=0
    false_count=0
    key = [['result of test'], ['🔙 Back to main menu']]
    reply_key = ReplyKeyboardMarkup(key, one_time_keyboard=True)
    update.message.reply_text(
        'Hey, please send the topic name in the correct format (e.g., topic_name?).',
        reply_markup=reply_key
    )


def quiz_test(update, context):
    global text, j,true_count,false_count
    true_count=0
    false_count=0
    matn = update.message.text.replace('?', '').strip().lower()


   
    text = matn

    count = any(i.get('topic_name') == matn for i in res.all())

    if count:
        update.message.reply_text(f'We started the topic "{matn}". If you are ready, send "begin".')
    else:
        update.message.reply_text(f'I cannot find the topic "{matn}".')


def get_answer(update, context):
    global result, text, j,true_count,false_count
    true_count=0
    false_count=0
    number = []
    db = TinyDB(f'{text}.json')
    matn = update.message.text.lower()
    user_id = update.message.from_user.id
    user_data = result.get(doc_id=user_id)

    if user_data:
        user_data["answers"].append(matn.lower())
        result.update({'answers': user_data["answers"]}, doc_ids=[user_id])
    else:
        result.insert({'user_id': user_id, 'answers': [matn]})

    
    questions = db.all()

    for i in questions:
        term = i.get('term')
        number.append(term)

    answer_db = result.all()
    for i in answer_db:
        user_answers = i['answers']
        for answer in user_answers:
            if answer in number:
                true_count += 1
            else:
                false_count += 1

    
   
    j.insert({'user_id': user_id, 'true_count': true_count, 'false_count': false_count})
    print(j.all()[-1])
    print(true_count)
    print(false_count)
   


def ask_question(update, context):
    global text, j,true_count,false_count
    true_count=0
    false_count=0
    db = TinyDB(f'{text}.json')
    records = db.all()
    index = 0

    while index < len(records):
        update.message.reply_text(f'{index + 1} topic: {text} Question: {records[index].get("definition")}')

        user_input = update.message.text.lower()

        if user_input == 'exit':
            update.message.reply_text("Quiz finished.")
            break

        time.sleep(10)
        index += 1
    last_quiz( update,context)

def last_quiz(update, context):
    global j, text
    print(j.all())  # Bazada ma’lumot bormi, tekshiramiz
    
   

    javob = j.all()[-1]

    update.message.reply_text(
        f"Your {text} topic answers:\nTrue answers: {javob['true_count']}\nFalse answers: {javob['false_count']}"
    )

    # Ma’lumot o‘chirilishidan oldin yana tekshirib ko‘ring
    print("Natijalar chiqarildi, endi truncate ishlaydi")
    j.truncate()

def javob_chiqar(update, context):
    global j
    print(j.all())
