from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3

# دالة لإنشاء قاعدة البيانات
async def create_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    await update.message.reply_text("تم إنشاء قاعدة البيانات والجدول بنجاح!")

# إعداد البوت
def main():
    app = ApplicationBuilder().token("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc").build()

    app.add_handler(CommandHandler("create_db", create_db))

    app.run_polling()

if __name__ == '__main__':
    main()
