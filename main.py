import logging
import os
import subprocess
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()  # تحميل المتغيرات البيئية

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('أرسل لي ملفاً لتنفيذ الكود!')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.document.get_file()
    await file.download_to_drive('code.py')

    try:
        result = subprocess.run(['python', 'code.py'], capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr

        # تنفيذ main.py بعد code.py
        result_main = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
        output_main = result_main.stdout if result_main.stdout else result_main.stderr

        await update.message.reply_text(f'نتيجة تنفيذ code.py:\n{output}\n\nنتيجة تنفيذ main.py:\n{output_main}')
    except Exception as e:
        await update.message.reply_text(f'حدث خطأ: {e}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()
