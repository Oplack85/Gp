import telebot
import requests

# ضع هنا التوكن الخاص بالبوت الذي حصلت عليه من BotFather
API_TOKEN = '7218686976:AAHKUWhhQFNIPfr12Yg0v08g7bti8OPdXsA'

# إنشاء البوت باستخدام التوكن
bot = telebot.TeleBot(API_TOKEN)

# متغير لتخزين الإيميل الوهمي لكل مستخدم
user_emails = {}

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

# عند بدء المحادثة مع البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! سأقوم بجلب إيميلات وهمية ورسائلها.")

# عند طلب المستخدم جلب إيميل وهمي
@bot.message_handler(commands=['getemail'])
def send_fake_email(message):
    email = get_fake_email()
    user_emails[message.chat.id] = email  # تخزين الإيميل للمستخدم
    bot.reply_to(message, f"إيميل وهمي تم إنشاؤه: {email}\nاستخدم /getmessages لجلب الرسائل.")

# عند طلب المستخدم جلب الرسائل للإيميل الوهمي
@bot.message_handler(commands=['getmessages'])
def send_fake_email_messages(message):
    email = user_emails.get(message.chat.id)  # الحصول على الإيميل الوهمي المخزن للمستخدم

    if not email:
        bot.reply_to(message, "لم تقم بإنشاء إيميل وهمي بعد. استخدم /getemail لإنشاء واحد.")
        return

    messages = get_messages_from_email(email)

    if messages:
        for msg in messages:
            subject = msg.get('subject', 'لا يوجد موضوع')  # تحقق من وجود 'subject'
            sender = msg.get('from', 'غير معروف')  # تحقق من وجود 'from'
            # تحقق من وجود 'textBody' أو استخدم 'htmlBody' كبديل
            body = msg.get('textBody') or msg.get('htmlBody') or 'المحتوى غير متاح'

            bot.reply_to(message, f"رسالة جديدة:\nالموضوع: {subject}\nالمرسل: {sender}\nالمحتوى: {body}")
    else:
        bot.reply_to(message, "لا توجد رسائل حالياً.")

# تشغيل البوت
bot.infinity_polling()
