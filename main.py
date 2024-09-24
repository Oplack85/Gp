from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3

async def create_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    
    await update.message.reply_text("تم إنشاء قاعدة البيانات والجدول بنجاح!")

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("يرجى إدخال الاسم والعمر. مثال: /add_user Alice 30")
        return
    
    name = context.args[0]
    age = int(context.args[1])

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"تم إضافة المستخدم: {name}, العمر: {age}.")

async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    conn.close()

    if rows:
        message = "\n".join([f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}" for row in rows])
    else:
        message = "لا توجد بيانات في قاعدة البيانات."

    await update.message.reply_text(message)

def main():
    app = ApplicationBuilder().token("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc").build()

    app.add_handler(CommandHandler("create_db", create_db))
    app.add_handler(CommandHandler("add_user", add_user))
    app.add_handler(CommandHandler("show_data", show_data))

    app.run_polling()

if __name__ == '__main__':
    main()
    
