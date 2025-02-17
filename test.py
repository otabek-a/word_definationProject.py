from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import wikipediaapi
from telegram import ReplyKeyboardMarkup
from tinydb import TinyDB
import time

res = TinyDB("topics.json")
text = ''
result=TinyDB('javob.json')
def test_data(update, context):
    key = [['result of test'], ['🔙 Back to main menu']]
    reply_key = ReplyKeyboardMarkup(key, one_time_keyboard=True)
    update.message.reply_text(
        'Hey, please send the topic name in the correct format (e.g., topic_name?).',
        reply_markup=reply_key
    )

def quiz_test(update, context):
    global text
    matn = update.message.text.replace('?', '').strip().lower()
    text = matn
    count = any(i.get('topic_name') == matn for i in res.all())


    if count:
        update.message.reply_text(f'We started the topic "{matn}". If you are ready, send "begin".')
    else:
        update.message.reply_text(f'I cannot find the topic "{matn}".')

def ask_question(update, context):
    global text
    db = TinyDB(f'{text}.json')
    records = db.all()
    index = 0
    








    
    
    while index < len(records):
        update.message.reply_text(f'{index+1} topic: {text} Question: {records[index].get("definition")}')
        if index==len(records):
            text=f'Your {text} topic answers:\n'

        user_input=update.message.text
        
        if user_input.lower() == 'exit':
            update.message.reply_text("Quiz finished.")
            break
        time.sleep(10)
        index+=1
def get_answer(update, context):
    global result, text
    db = TinyDB(f'{text}.json')
    matn = update.message.text.lower()
    user_id = update.message.from_user.id

    # Foydalanuvchi javoblarini olish yoki yangilash
    user_data = result.get(doc_id=user_id)

    if user_data:
        user_data["answers"].append(matn)
        result.update({'answers': user_data["answers"]}, doc_ids=[user_id])
    else:
        result.insert({'user_id': user_id, 'answers': [matn]})

    true_count = 0
    false_count = 0

    # To'g'ri javoblarni olish
    question_db = db.all()
    correct_answers = [record.get('term').lower() for record in question_db]  # To'g'ri javoblarni olish

    # Foydalanuvchi javoblarini olish
    user_data = result.get(doc_id=user_id)
    user_answers = user_data.get('answers', [])  # Agar javoblar bo‘lmasa, bo‘sh ro‘yxat olish

    # Har bir foydalanuvchi javobini tekshirish
    for answer in user_answers:
        if answer in correct_answers:
            true_count += 1
        else:
            false_count += 1

    # Agar foydalanuvchi ba'zi savollarga javob bermagan bo‘lsa, ularni noto‘g‘ri (`false`) deb hisoblash
    if len(user_answers) < len(correct_answers):
        false_count += len(correct_answers) - len(user_answers)

    # Natijalarni yangilash (insert emas, update ishlatiladi)
    tekshir = TinyDB('savol.json')
    existing_record = tekshir.get(doc_id=user_id)

    if existing_record:
        tekshir.update({'true': true_count, 'false': false_count}, doc_ids=[user_id])
    else:
        tekshir.insert({'user_id': user_id, 'true': true_count, 'false': false_count})

    update.message.reply_text(f"Your results:\n✅ Correct: {true_count}\n❌ Incorrect (including unanswered): {false_count}")
    print(tekshir.all())
