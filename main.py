import telebot
import requests
import time
import threading
from bs4 import BeautifulSoup

# ضع هنا التوكن الخاص بالبوت
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

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
                # التأكد من أن الرسالة جديدة ولم يتم عرضها من قبل
                if chat_id not in user_messages:
                    user_messages[chat_id] = []
                if message_id not in user_messages[chat_id]:
                    subject = msg.get('subject', 'لا يوجد موضوع')
                    sender = msg.get('from', 'غير معروف')
                    
                    # جلب محتويات الرسالة بالتفصيل باستخدام ID الرسالة
                    full_message = get_message_content(email, message_id)
                    
                    # عرض محتويات الرسالة كاملة في logs لفحص الحقول
                    print(f"Full message content: {full_message}")
                    
                    # محاولة جلب النص العادي أو استخدام HTML إذا لم يكن النص متاحًا
                    body = full_message.get('textBody')
                    if not body:  # إذا لم يكن هناك نص عادي، نستخدم htmlBody
                        body = full_message.get('htmlBody', 'المحتوى غير متاح')
                        # تحويل HTML إلى نص عادي إذا كان متاحاً
                        if body != 'المحتوى غير متاح':
                            body = html_to_text(body)

                    bot.send_message(chat_id, f"رسالة جديدة:\nالموضوع: {subject}\nالمرسل: {sender}\nالمحتوى: {body}")
                    # حفظ معرف الرسالة لتجنب التكرار
                    user_messages[chat_id].append(message_id)
        time.sleep(10)  # الانتظار لمدة 10 ثوانٍ قبل التحقق مرة أخرى

# عند بدء المحادثة مع البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! سأقوم بجلب إيميلات وهمية ومتابعة رسائلها الواردة.")

# عند طلب المستخدم جلب إيميل وهمي
@bot.message_handler(commands=['getemail'])
def send_fake_email(message):
    email = get_fake_email()
    user_emails[message.chat.id] = email  # تخزين الإيميل للمستخدم
    bot.reply_to(message, f"إيميل وهمي تم إنشاؤه: {email}\nسيتم الآن متابعة الرسائل الجديدة.")
    
    # بدء عملية مراقبة الرسائل في صندوق الوارد
    email_thread = threading.Thread(target=check_for_new_messages, args=(message.chat.id, email))
    email_thread.daemon = True
    email_thread.start()

# تشغيل البوت
bot.infinity_polling()
