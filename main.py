import telebot
import requests

# ضع هنا التوكن الخاص بالبوت الذي حصلت عليه من BotFather
API_TOKEN = '7218686976:AAH3doF67rbhtGGEbiIVn_XgxdYPcTxE5uI'

# إنشاء البوت باستخدام توكن
bot = telebot.TeleBot(API_TOKEN)

# دالة لجلب الإيميل الوهمي من 1secmail
def get_fake_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox')
    email = response.json()[0]
    return email

# دالة لجلب الرسائل الواردة على الإيميل الوهمي
def get_messages_from_email(email):
    user, domain = email.split('@')
    response = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}')
    messages = response.json()
    return messages

# عندما يبدأ المستخدم محادثة مع البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! سأقوم بجلب إيميلات وهمية ورسائلها.")

# عندما يرسل المستخدم "/getemail"
@bot.message_handler(commands=['getemail'])
def send_fake_email(message):
    email = get_fake_email()
    bot.reply_to(message, f"إيميل وهمي تم إنشاؤه: {email}")

# عندما يرسل المستخدم "/getmessages"
@bot.message_handler(commands=['getmessages'])
def send_fake_email_messages(message):
    try:
        # قم بجلب الإيميل الوهمي
        email = get_fake_email()

        # جلب الرسائل الواردة على الإيميل
        messages = get_messages_from_email(email)

        if messages:
            for msg in messages:
                bot.reply_to(message, f"رسالة جديدة: \nالموضوع: {msg['subject']}\nالمرسل: {msg['from']}\nالمحتوى: {msg['textBody']}")
        else:
            bot.reply_to(message, "لا توجد رسائل حالياً.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")

# تشغيل البوت
bot.infinity_polling()
