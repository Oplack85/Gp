import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube

load_dotenv()  # تحميل المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN")  # استرجاع توكن البوت

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أرسل لي رابط الفيديو من يوتيوب وسأقوم بتنزيله لك!')

def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()
        update.message.reply_text(f'تم تنزيل الفيديو: {yt.title}')
    except Exception as e:
        update.message.reply_text('حدث خطأ: ' + str(e))

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
