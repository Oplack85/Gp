import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pytube import YouTube

load_dotenv()  # تحميل المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")  # استرجاع توكن البوت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('أرسل لي رابط الفيديو من يوتيوب وسأقوم بتنزيله لك!')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()
        await update.message.reply_text(f'تم تنزيل الفيديو: {yt.title}')
    except Exception as e:
        await update.message.reply_text('حدث خطأ: ' + str(e))

async def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
