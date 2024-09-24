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
# متغير لتخزين قائمة الإيميلات لكل مستخدم
user_email_list = {}

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
                        if body != '✎┊‌ الرسالة فارغه':
                            body = html_to_text(body)
                    
                    bot.send_message(chat_id, body)  # إرسال محتوى الرسالة فقط
                    user_messages[chat_id].append(message_id)
        time.sleep(10)  # الانتظار لمدة 10 ثوانٍ قبل التحقق مرة أخرى

# عند بدء المحادثة مع البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_email = types.KeyboardButton("إنشاء إيميل")
    button_list_emails = types.KeyboardButton("عرض الإيميلات")
    markup.add(button_email, button_list_emails)
    bot.send_message(message.chat.id, "[𝗦𝗖 𝗙𝗮𝗸𝗲 𝗠𝗮𝗶𝗟 📮](https://t.me/Scorpion_scorp)\n\n*✎┊‌ مرحبا بك في بوت الايميلات الوهمية 👋🏻*\n\n*للحصول على ايميل اضغط على انشاء ايميل ✍🏻* \n\n* تم تطوير البوت بواسطة :* \n*المطور* [𝗠𝗼𝗵𝗮𝗺𝗲𝗱](t.me/Zo_r0) \n*المطور* [𝗔𝗹𝗹𝗼𝘂𝘀𝗵](t.me/I_e_e_l)", reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

# عرض قائمة الإيميلات
@bot.message_handler(func=lambda message: message.text == "عرض الإيميلات")
def show_email_list(message):
    chat_id = message.chat.id
    emails = user_email_list.get(chat_id, [])
    if emails:
        email_list_str = "\n".join([f"{i+1}. {email}" for i, email in enumerate(emails)])
        bot.send_message(chat_id, f"*✎┊‌ قائمة الإيميلات:*\n\n{email_list_str}", parse_mode='Markdown')
    else:
        bot.send_message(chat_id, "*✎┊‌ لا توجد إيميلات تم إنشاؤها بعد.*", parse_mode='Markdown')

# حذف إيميل محدد
@bot.message_handler(commands=['delete_email'])
def delete_email(message):
    chat_id = message.chat.id
    emails = user_email_list.get(chat_id, [])
    
    if not emails:
        bot.send_message(chat_id, "*✎┊‌ لا توجد إيميلات لحذفها.*", parse_mode='Markdown')
        return

    try:
        # طلب رقم الإيميل المراد حذفه
        email_number = int(message.text.split()[1]) - 1
        if 0 <= email_number < len(emails):
            deleted_email = emails.pop(email_number)
            user_email_list[chat_id] = emails  # تحديث القائمة
            bot.send_message(chat_id, f"*✎┊‌ تم حذف الإيميل: {deleted_email}* ✅", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "*✎┊‌ رقم الإيميل غير صحيح.*", parse_mode='Markdown')
    except (IndexError, ValueError):
        bot.send_message(chat_id, "*✎┊‌ يرجى إدخال رقم الإيميل الصحيح بعد الأمر.*\n*مثال: *`/delete_email 1`", parse_mode='Markdown')

# عند الضغط على زر إنشاء إيميل
@bot.message_handler(func=lambda message: message.text == "إنشاء إيميل")
def send_fake_email(message):
    email = get_fake_email()
    chat_id = message.chat.id
    user_emails[chat_id] = email
    if chat_id not in user_email_list:
        user_email_list[chat_id] = []
    user_email_list[chat_id].append(email)  # إضافة الإيميل للقائمة
    bot.reply_to(message, f"*✎┊‌ إيميل وهمي تم إنشاؤه ✅\n\nإضغط للنسخ [* `{email}` *]\n\n✎┊‌ عزيزي اي طلب او رسالة تجي عل ايميل راح تندز مباشرة مراح تحتاج جلب رسالة وغيرها *", parse_mode='Markdown')

    # بدء عملية مراقبة الرسائل في صندوق الوارد
    email_thread = threading.Thread(target=check_for_new_messages, args=(chat_id, email))
    email_thread.daemon = True
    email_thread.start()

# تشغيل البوت
bot.infinity_polling()
