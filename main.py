import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

# حالات المحادثة
EMAIL = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("استنساخ البريد", callback_data='clone_email')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('اضغط على الزر لاستنساخ البريد:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'clone_email':
        await query.edit_message_text(text='يرجى إدخال البريد الإلكتروني الذي تريد استنساخه:')
        return EMAIL

async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    original_email = update.message.text
    copies = [f"{original_email.split('@')[0]}+{i}@{original_email.split('@')[1]}" for i in range(1, 51)]
    
    # هنا يمكنك تنفيذ أي منطق إضافي لجعل كل نسخة تعمل بشكل مستقل
    for copy in copies:
        # يمكنك إجراء عملية إضافية مع كل نسخة، مثل إرسالها إلى واجهة برمجة تطبيقات أو قاعدة بيانات
        await update.message.reply_text(f'تم إنشاء النسخة: {copy}')

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('تم إلغاء العملية.')
    return ConversationHandler.END

def main():
    # الحصول على توكن البوت من المتغير البيئي
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    application = ApplicationBuilder().token(token).build()

    # إعداد ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # إضافة المعالجات
    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)

    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    main()
