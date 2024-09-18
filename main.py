import telebot
import os
from gpt import gpt

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['openai'])
def openai_command(message):
    bot.send_message(message.chat.id, "اكتب سؤالك وسأجيب عليه إن شاء الله.")

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    try:
        # إرسال الرسالة إلى دالة gpt واستلام الرد
        resp = gpt(message.text)
        bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')
    except Exception as e:
        # التعامل مع الأخطاء وإرسال رسالة تنبيهية
        bot.send_message(message.chat.id, f'حدث خطأ: {e}', parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
