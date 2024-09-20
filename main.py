import os
import telebot
import pytgpt.phind

# ضع توكن البوت هنا
TOKEN = '7218686976:AAH3doF67rbhtGGEbiIVn_XgxdYPcTxE5uI'

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

# إعداد GPT
gpt_bot = pytgpt.phind.PHIND()

def gpt(message):
    return gpt_bot.chat(f'{message}')

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    if message.text.startswith('/Gpt'):
        question = message.text[4:]  # استخرج السؤال بعد الأمر /Gpt
        resp = gpt(question)
        bot.send_message(message.chat.id, f'Gpt : {resp}', parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
