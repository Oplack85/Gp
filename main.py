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
        # تنفيذ code.py في الخلفية
        process_code = subprocess.Popen(['python', 'code.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_code, stderr_code = process_code.communicate()

        output_code = stdout_code.decode() if stdout_code else stderr_code.decode()
        
        await update.message.reply_text(f'نتيجة تنفيذ code.py:\n{output_code}')
    except Exception as e:
        await update.message.reply_text(f'حدث خطأ: {e}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()
    
