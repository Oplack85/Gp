import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator
import random
import nltk

# ضع رمز API للبوت هنا
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = telebot.TeleBot(TOKEN)
translator = GoogleTranslator(source='en', target='ar')
current_word = ''
difficulty_level = ''

# تحميل الموارد اللازمة من مكتبة nltk
nltk.download('words')
from nltk.corpus import words

# إنشاء قوائم الكلمات بناءً على مستوى الصعوبة
easy_words = [word for word in words.words() if 2 <= len(word) <= 4]
medium_words = [word for word in words.words() if 4 <= len(word) <= 7]
hard_words = [word for word in words.words() if len(word) > 7]

# اختيار كلمة عشوائية بناءً على مستوى الصعوبة
def get_random_word(level):
    if level == 'easy':
        return random.choice(easy_words)
    elif level == 'medium':
        return random.choice(medium_words)
    elif level == 'hard':
        return random.choice(hard_words)

# بدء المحادثة وتحديد مستوى الصعوبة
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("سهل", callback_data='easy'),
        InlineKeyboardButton("متوسط", callback_data='medium'),
        InlineKeyboardButton("صعب", callback_data='hard')
    )
    bot.send_message(message.chat.id, "اختر مستوى الصعوبة:", reply_markup=markup)

# معالجة اختيار مستوى الصعوبة
@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'medium', 'hard'])
def set_difficulty(call):
    global difficulty_level
    difficulty_level = call.data
    bot.answer_callback_query(call.id, f'تم اختيار المستوى: {difficulty_level.capitalize()}')
    send_random_word(call.message)

# إرسال كلمة عشوائية بناءً على مستوى الصعوبة
def send_random_word(message):
    global current_word, difficulty_level
    current_word = get_random_word(difficulty_level)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("ترجمة الكلمة", callback_data='translate'))
    bot.send_message(message.chat.id, f'ما هي ترجمة الكلمة التالية: {current_word}؟', reply_markup=markup)

# التحقق من الإجابة
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    global current_word
    user_answer = message.text.lower()
    translation = translator.translate(current_word).lower()

    if user_answer == translation:
        bot.send_message(message.chat.id, 'إجابة صحيحة! 🎉')
    else:
        bot.send_message(message.chat.id, f'إجابة خاطئة! الترجمة الصحيحة هي: {translation}')

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
    bot.send_message(call.message.chat.id, f'ترجمة الكلمة "{current_word}" هي: {translation}', reply_markup=markup)

# إعطاء كلمة جديدة من نفس المستوى عند اختيار "كلمة أخرى"
@bot.callback_query_handler(func=lambda call: call.data == 'another_word')
def another_word(call):
    bot.answer_callback_query(call.id)
    send_random_word(call.message)

# بدء البوت
bot.polling()
