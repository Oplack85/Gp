import telebot
import os
from gpt import gpt

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    if message.text.startswith('/p '):
        question = message.text[3:]  # استخرج السؤال بعد الأمر /p
        try:
            # إرسال الرسالة إلى دالة gpt واستلام الرد
            resp = gpt(question)
            bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')
        except Exception as e:
            # التعامل مع الأخطاء وإرسال رسالة تنبيهية
            bot.send_message(message.chat.id, f'حدث خطأ: {e}', parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "يرجى استخدام الأمر /p متبوعًا بسؤالك.")

# بدء الاستماع للرسائل
bot.infinity_polling()
