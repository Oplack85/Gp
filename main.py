import os
import telebot
import pytgpt.phind

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TG_BOT_TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

# إعداد GPT
gpt_bot = pytgpt.phind.PHIND()

def gpt(message):
    return gpt_bot.chat(f'{message}')

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    if message.text.startswith('/p '):
        question = message.text[3:]  # استخرج السؤال بعد الأمر /p
        resp = gpt(question)  # أزل معالجة الأخطاء
        bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
