import telebot
import os
import sys
from gpt import gpt

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TG_BOT_TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['openai'])
def openai_command(message):
    bot.send_message(message.chat.id, '<b>✎┊‌ يمكنك الآن إرسال سؤالك.</b>')

@bot.message_handler(commands=['closeai'])
def stop_bot(message):
    bot.send_message(message.chat.id, '<b>✎┊‌ سيتم إيقاف البوت الآن.</b>')
    sys.exit()

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    if message.reply_to_message and message.reply_to_message.text == '<b>✎┊‌ يمكنك الآن إرسال سؤالك.</b>':
        try:
            # إرسال الرسالة إلى دالة gpt واستلام الرد
            resp = gpt(message.text)
            bot.send_message(message.chat.id, f'<b>{resp}</b>', parse_mode='HTML')
        except Exception as e:
            # التعامل مع الأخطاء وإرسال رسالة تنبيهية
            bot.send_message(message.chat.id, f'حدث خطأ: {e}', parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, 'يرجى استخدام الأمر /openai لبدء التفاعل.')

# بدء الاستماع للرسائل
bot.infinity_polling()
