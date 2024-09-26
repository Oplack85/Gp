from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

# حالات المحادثة
EMAIL, CONFIRM = range(2)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("استنساخ البريد", callback_data='clone_email')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اضغط على الزر لاستنساخ البريد:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'clone_email':
        query.edit_message_text(text='يرجى إدخال البريد الإلكتروني الذي تريد استنساخه:')
        return EMAIL

def receive_email(update: Update, context: CallbackContext) -> int:
    original_email = update.message.text
    # هنا يمكنك إضافة منطق لنسخ البريد إلى 50 نسخة
    # مثلاً: for i in range(1, 51):  نسخ البريد
    update.message.reply_text(f'تم استنساخ البريد: {original_email} إلى 50 نسخة.')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('تم إلغاء العملية.')
    return ConversationHandler.END

def main():
    # استبدل 'YOUR_TOKEN' برمز التوكن الخاص بك
    updater = Updater("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc")

    # إعداد ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, receive_email)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # إضافة المعالجات
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(conv_handler)

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
