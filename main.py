import telebot
import requests
import time
import threading
from bs4 import BeautifulSoup
from telebot import types

# ضع هنا التوكن الخاص بالبوت
API_TOKEN = '7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc'

# إنشاء البوت باستخدام التوكن
bot = telebot.TeleBot(API_TOKEN)

# متغير لتخزين الإيميل الوهمي لكل مستخدم
user_emails = {}
# متغير لتخزين الرسائل المستلمة لكل مستخدم لمنع التكرار
user_messages = {}

# دالة لجلب إيميل وهمي من 1secmail
def get_fake_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox')
    email = response.json()[0]
    return email

# دالة لجلب الرسائل الواردة على الإيميل الوهمي
def get_messages_from_email(email):
    user, domain = email.split('@')
    response = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}')
    return response.json()

# دالة لجلب محتوى رسالة معينة من ID
def get_message_content(email, message_id):
    user, domain = email.split('@')
    response = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={message_id}')
    return response.json()

# دالة لتحويل HTML إلى نص عادي
def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

# دالة لمراقبة البريد الإلكتروني للمستخدم
def check_for_new_messages(chat_id, email):
    while True:
        messages = get_messages_from_email(email)
        if messages:
            for msg in messages:
                message_id = msg['id']
                if chat_id not in user_messages:
                    user_messages[chat_id] = []
                if message_id not in user_messages[chat_id]:
                    full_message = get_message_content(email, message_id)
                    body = full_message.get('textBody')
                    if not body:
                        body = full_message.get('htmlBody', '✎┊‌ الرسالة فارغه')
                        if body != '✎┊‌ الرسالة فارغه ':
                            body = html_to_text(body)

                    bot.send_message(chat_id, body)  # إرسال محتوى الرسالة فقط
                    user_messages[chat_id].append(message_id)
        time.sleep(10)  # الانتظار لمدة 10 ثوانٍ قبل التحقق مرة أخرى

# عند بدء المحادثة مع البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_email = types.KeyboardButton("إنشاء إيميل")
    markup.add(button_email)
    
    channel_markup = types.InlineKeyboardMarkup()
    button_channel = types.InlineKeyboardButton("اشتراك في القناة", url="https://t.me/YourChannelLink")  # استبدل الرابط برابط قناتك
    channel_markup.add(button_channel)

    bot.send_message(message.chat.id, "*✎┊‌ مرحبا بك عزيزي في بوت الايميلات الوهميه*\n*الخاص بسورس العقرب ✓*\n\n*فقط اضغط على الزر أدناه لإنشاء إيميل 😊*\n\n*للاشتراك في القناة اضغط الزر أدناه:*", reply_markup=markup, parse_mode='Markdown')
# عند الضغط على زر إنشاء إيميل
@bot.message_handler(func=lambda message: message.text == "إنشاء إيميل")
def send_fake_email(message):
    email = get_fake_email()
    user_emails[message.chat.id] = email  # تخزين الإيميل للمستخدم
    bot.reply_to(message, f"*✎┊‌ إيميل وهمي تم إنشاؤه*\n*إضغط للنسخ [ `{email}` ]*\n*✎┊‌ عزيزي اي طلب او رساله تجي عل ايميل راح تندز مباشرة مراح تحتاج جلب رسالة وغيرها ✓*", parse_mode='Markdown')
    
    # بدء عملية مراقبة الرسائل في صندوق الوارد
    email_thread = threading.Thread(target=check_for_new_messages, args=(message.chat.id, email))
    email_thread.daemon = True
    email_thread.start()

# تشغيل البوت
bot.infinity_polling()
