import os
import requests
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)

# الحصول على التوكن من المتغيرات البيئية
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# دالة لجلب إيميل مؤقت من 10MinuteMail
def get_temp_email():
    response = requests.get("https://10minutemail.com/session/address")
    if response.status_code == 200:
        email_data = response.json()
        email_address = email_data['address']  # جلب الإيميل من البيانات المستلمة
        return email_address
    else:
        return None

# دالة لجلب الرسائل الواردة
def get_inbox(email_address):
    inbox_url = "https://10minutemail.com/session/messages"
    response = requests.get(inbox_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# دالة لبدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("جلب إيميل وهمي", callback_data='get_email')],
        [InlineKeyboardButton("جلب الرسائل", callback_data='get_inbox')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('أهلاً بك! اختر أحد الخيارات:', reply_markup=reply_markup)

# دالة لتنفيذ الأوامر عند الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'get_email':
        email = get_temp_email()
        if email:
            context.user_data['email'] = email  # تخزين الإيميل للاستخدام لاحقًا
            await query.edit_message_text(f"تم إنشاء إيميل وهمي: {email}")
        else:
            await query.edit_message_text("فشل في جلب الإيميل الوهمي.")
    
    elif query.data == 'get_inbox':
        email = context.user_data.get('email')
        if email:
            inbox = get_inbox(email)
            if inbox:
                message_list = "\n".join([message['message'] for message in inbox])
                await query.edit_message_text(f"الرسائل الواردة:\n{message_list}")
            else:
                await query.edit_message_text("لا توجد رسائل واردة بعد.")
        else:
            await query.edit_message_text("يرجى جلب الإيميل أولاً باستخدام الزر المخصص.")

# إعداد Webhook
@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    update = Update.de_json(update, app.bot)
    app.bot.process_update(update)
    return 'ok'

# تشغيل البوت
def main():
    app.bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.bot.add_handler(CommandHandler("start", start))
    app.bot.add_handler(CallbackQueryHandler(button_handler))

    # تشغيل Webhook
    app.bot.run_webhook(listen="0.0.0.0",
                        port=int(os.environ.get('PORT', 8443)),
                        url_path=TELEGRAM_BOT_TOKEN,
                        webhook_url=f"https://YOUR_WEBHOOK_URL/{TELEGRAM_BOT_TOKEN}")

if __name__ == '__main__':
    main()
    app.run(port=int(os.environ.get('PORT', 8443)))
    
