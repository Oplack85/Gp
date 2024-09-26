import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# دالة لتنفيذ ملف sh
def run_script(update: Update, context: CallbackContext) -> None:
    try:
        # اسم الملف
        script_file = 'pt.sh'
        # تنفيذ السكربت
        result = subprocess.run(['bash', script_file], capture_output=True, text=True)
        # كتابة النتائج في ملف
        with open('result.txt', 'w') as f:
            f.write(result.stdout)
        # إرسال النتائج للمستخدم
        with open('result.txt', 'rb') as f:
            context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    except Exception as e:
        update.message.reply_text(f"حدث خطأ: {str(e)}")

def main():
    # إدخال توكن البوت
    updater = Updater("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("run", run_script))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
