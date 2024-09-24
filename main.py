from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import psycopg2
import uuid

# إعداد الاتصال بقاعدة البيانات
def create_db_connection():
    return psycopg2.connect(
        dbname="koyebdb",
        user="koyeb-adm",
        password="cPAZfq2Gsa0w",
        host="ep-fancy-poetry-a4dstf74.us-east-1.pg.koyeb.app",
        port="5432"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحباً! استخدم /create_db لإنشاء قاعدة بيانات جديدة.")

async def create_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db_name = f"db_{uuid.uuid4().hex}"  # إنشاء اسم قاعدة بيانات فريد
    try:
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name};")
        conn.commit()
        await update.message.reply_text(f"تم إنشاء قاعدة البيانات: {db_name}")
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")
    finally:
        cursor.close()
        conn.close()

def main() -> None:
    app = ApplicationBuilder().token("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create_db", create_db))

    app.run_polling()

if __name__ == '__main__':
    main()
    
