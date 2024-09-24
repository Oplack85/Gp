from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import sqlite3

# دالة لإنشاء قاعدة البيانات
def create_db(update: Update, context: CallbackContext):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    
    # مثال على إنشاء جدول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    
    update.message.reply_text("تم إنشاء قاعدة البيانات والجدول بنجاح!")

# إعداد البوت
def main():
    updater = Updater("YOUR_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("create_db", create_db))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
