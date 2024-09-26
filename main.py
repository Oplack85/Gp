import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

# حالات المحادثة
EMAIL, NUMBER = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("استنساخ البريد", callback_data='clone_email')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('✎┊‌ اضغط على الزر لاستنساخ البريد:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'clone_email':
        await query.edit_message_text(text='✎┊‌ يرجى إدخال البريد الإلكتروني الذي تريد استنساخه:')
        return EMAIL

async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    original_email = update.message.text
    await update.message.reply_text('✎┊‌ يرجى إدخال عدد النسخ (حد أقصى 1000):')
    context.user_data['original_email'] = original_email
    return NUMBER

async def receive_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        num_copies = int(update.message.text)
        if 1 <= num_copies <= 1000:
            original_email = context.user_data['original_email']
            copies = [f"{i}) {original_email}" for i in range(1, num_copies + 1)]
            
            # تقسيم النسخ إلى مجموعات وإرسال كل مجموعة في رسالة منفصلة
            chunk_size = 50  # عدد النسخ في كل رسالة
            for i in range(0, len(copies), chunk_size):
                copies_text = "\n".join(copies[i:i + chunk_size])
                await update.message.reply_text(f'✎┊‌ تم إنشاء النسخ التالية:\n\n{copies_text}')
        else:
            await update.message.reply_text('✎┊‌ يرجى إدخال رقم بين 1 و 1000.')
            return NUMBER

    except ValueError:
        await update.message.reply_text('✎┊‌ يرجى إدخال عدد صحيح.')
        return NUMBER

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
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_number)],
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
            
