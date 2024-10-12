import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from random_words import RandomWords
from googletrans import Translator

# ضع رمز API للبوت هنا
TOKEN = '7218686976:AAHn7mwAZQUjLxBWVtanhR5Tqc9O38INcCs'

bot = telebot.TeleBot(TOKEN)
rw = RandomWords()
translator = Translator()
current_word = ''
difficulty_level = ''

# توليد قوائم الكلمات بناءً على مستوى الصعوبة
def get_random_word(level):
    while True:
        word = rw.random_word()
        if level == 'easy' and len(word) <= 4:
            return word
        elif level == 'medium' and 5 <= len(word) <= 7:
            return word
        elif level == 'hard' and len(word) > 7:
            return word

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
    translation = translator.translate(current_word, dest='ar').text.lower()

    if user_answer == translation:
        bot.send_message(message.chat.id, 'إجابة صحيحة! 🎉')
    else:
        bot.send_message(message.chat.id, f'إجابة خاطئة! الترجمة الصحيحة هي: {translation}')

    send_random_word(message)

# ترجمة الكلمة وعرض زر "كلمة أخرى"
@bot.callback_query_handler(func=lambda call: call.data == 'translate')
def translate_word(call):
    global current_word
    translation = translator.translate(current_word, dest='ar').text

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
