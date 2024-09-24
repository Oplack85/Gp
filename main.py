from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import psycopg2
import os

# إعداد الاتصال بقاعدة البيانات
def create_db_connection():
    conn = psycopg2.connect(
        dbname="koyebdb",
        user="koyeb-adm",
        password="cPAZfq2Gsa0w",
        host="ep-fancy-poetry-a4dstf74.us-east-1.pg.koyeb.app",
        port="5432"
    )
    return conn

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("مرحباً! استخدم /create_db لإنشاء قاعدة بيانات جديدة.")

def create_db(update: Update, context: CallbackContext) -> None:
    try:
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE new_database;")
        conn.commit()
        update.message.reply_text("تم إنشاء قاعدة البيانات بنجاح!")
    except Exception as e:
        update.message.reply_text(f"حدث خطأ: {e}")
    finally:
        cursor.close()
        conn.close()

def main() -> None:
    updater = Updater("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_db", create_db))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
