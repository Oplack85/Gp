from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# استبدل هذا بالتوكن الخاص بالبوت
TOKEN = "7054581703:AAGdJvc9RxOXMZhjahLlSTUN4LHoi8zR9qw"

# أمر /start 
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("مرحبًا! أنا بوت حماية المجموعات.")

# أمر لإضافة مدير
async def add_admin(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("تم إضافة المدير بنجاح!")

# أمر لإزالة مستخدم
async def remove_user(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("تم إزالة المستخدم!")

# أمر للترحيب
async def welcome(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("مرحبًا بالمستخدم الجديد!")

# أمر للتبليغ عن مستخدم
async def report_user(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("تم التبليغ عن المستخدم.")

# الرد على الرسائل التي تحتوي على كلمات محظورة
async def filter_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    banned_words = ['كلمة1', 'كلمة2']  # أضف الكلمات المحظورة هنا
    if any(word in text for word in banned_words):
        await update.message.reply_text("تم اكتشاف كلمة محظورة!")

async def main() -> None:
    # إعداد التطبيق
    application = Application.builder().token(TOKEN).build()

    # أوامر البوت
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", add_admin))
    application.add_handler(CommandHandler("ban", remove_user))
    application.add_handler(CommandHandler("wel", welcome))
    application.add_handler(CommandHandler("repo", report_user))

    # فلترة الرسائل
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_message))

    # بدء تشغيل البوت
    await application.start()  # استبدل start_polling بـ start
    await application.updater.start_polling()  # إذا كنت تريد استخدام polling بشكل إضافي
    await application.updater.stop()  # لإيقافها عند الحاجة
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    
