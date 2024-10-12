import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
import random

# ضع رمز API للبوت هنا
TOKEN = '7218686976:AAHn7mwAZQUjLxBWVtanhR5Tqc9O38INcCs'

bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')  # استخدام Markdown لتنسيق الرسائل
translator = GoogleTranslator(source='en', target='ar')
current_word = ''
difficulty_level = ''
user_coins = {}  # قاموس لتتبع العملات الذهبية لكل مستخدم

# تحميل الكلمات من ملف النص وتصنيفها حسب الطول
def load_words_from_file(file_path='words_list.txt'):
    easy_words = []
    medium_words = []
    hard_words = []

    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            if 2 <= len(word) <= 4:
                easy_words.append(word)
            elif 4 < len(word) <= 7:
                medium_words.append(word)
            elif len(word) > 7:
                hard_words.append(word)

    return easy_words, medium_words, hard_words

# تحميل الكلمات بناءً على مستوى الصعوبة
easy_words, medium_words, hard_words = load_words_from_file()

# اختيار كلمة عشوائية بناءً على مستوى الصعوبة، مع التأكد من أنها مختلفة عن الكلمة السابقة
def get_random_word(level, previous_word):
    word_list = easy_words if level == 'easy' else medium_words if level == 'medium' else hard_words
    new_word = random.choice(word_list)
    while new_word == previous_word:  # ضمان عدم تكرار الكلمة السابقة
        new_word = random.choice(word_list)
    return new_word

# بدء المحادثة وتحديد مستوى الصعوبة
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_coins[user_id] = user_coins.get(user_id, 0)  # تهيئة العملات الذهبية للمستخدم إن لم تكن موجودة

    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("سهل", callback_data='easy'),
        InlineKeyboardButton("متوسط", callback_data='medium'),
        InlineKeyboardButton("صعب", callback_data='hard'),
        InlineKeyboardButton("💰 عملاتي", callback_data='my_coins')
    )
    bot.send_message(message.chat.id, f"*مرحباً بك! لديك {user_coins[user_id]} عملة ذهبية.*\n*اختر مستوى الصعوبة:*", reply_markup=markup)

# معالجة اختيار مستوى الصعوبة
@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'medium', 'hard'])
def set_difficulty(call):
    global difficulty_level
    difficulty_level = call.data

    # حذف رسالة الترحيب بعد اختيار المستوى
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    bot.answer_callback_query(call.id, f'*تم اختيار المستوى: {difficulty_level.capitalize()}*')
    send_random_word(call.message)

# إرسال كلمة عشوائية بناءً على مستوى الصعوبة
def send_random_word(message):
    global current_word, difficulty_level
    current_word = get_random_word(difficulty_level, current_word)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ترجمة الكلمة", callback_data='translate'))
    bot.send_message(message.chat.id, f'*ما هي ترجمة الكلمة التالية: {current_word}؟*', reply_markup=markup)

# التحقق من الإجابة
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global current_word
    user_id = message.from_user.id
    user_answer = message.text.lower()
    translation = translator.translate(current_word).lower()

    if user_answer == translation:
        user_coins[user_id] = user_coins.get(user_id, 0) + 1  # إضافة عملة ذهبية للمستخدم
        bot.send_message(message.chat.id, f'*إجابة صحيحة! 🎉 لقد حصلت على عملة ذهبية. الآن لديك {user_coins[user_id]} عملة ذهبية.*')
    else:
        bot.send_message(message.chat.id, f'*إجابة خاطئة! الترجمة الصحيحة هي: {translation}*')

    send_random_word(message)

# ترجمة الكلمة وعرض زر "كلمة أخرى"
@bot.callback_query_handler(func=lambda call: call.data == 'translate')
def translate_word(call):
    global current_word
    translation = translator.translate(current_word)

    # إضافة زر "كلمة أخرى" بعد الترجمة
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("كلمة أخرى", callback_data='another_word'))
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f'*ترجمة الكلمة "{current_word}" هي: {translation}*', reply_markup=markup)

# عرض العملات الذهبية للمستخدم
@bot.callback_query_handler(func=lambda call: call.data == 'my_coins')
def show_coins(call):
    user_id = call.from_user.id
    coins = user_coins.get(user_id, 0)
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f'*لديك {coins} عملة ذهبية.*')

# إعطاء كلمة جديدة من نفس المستوى عند اختيار "كلمة أخرى"
@bot.callback_query_handler(func=lambda call: call.data == 'another_word')
def another_word(call):
    bot.answer_callback_query(call.id)
    send_random_word(call.message)

# بدء البوت
bot.polling()
