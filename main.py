import logging
import os
import sys
import asyncio
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
        # تنفيذ code.py بشكل غير متزامن
        process = await asyncio.create_subprocess_exec(
            'python', 'code.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        output = stdout.decode() if stdout else stderr.decode()
        
        await update.message.reply_text(f'نتيجة تنفيذ code.py:\n{output}')
        
        # إعادة تشغيل البوت
        os.execv(sys.executable, ['python'] + sys.argv)
        
    except Exception as e:
        await update.message.reply_text(f'حدث خطأ: {e}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()
    
