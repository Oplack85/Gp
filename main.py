from pytube import YouTube
import instaloader
from tiktokapi import TikTokApi
import telebot
import os
from dotenv import load_dotenv

load_dotenv()  # تحميل المتغيرات البيئية

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أرسل لي رابط الفيديو لتحميله من يوتيوب أو إنستغرام أو تيك توك أو فيس بوك.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    try:
        if 'youtube.com' in url:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download()
            bot.reply_to(message, f"تم تحميل الفيديو من يوتيوب: {yt.title}")
        elif 'instagram.com' in url:
            loader = instaloader.Instaloader()
            loader.download_post(instaloader.Post.from_shortcode(loader.context, url.split('/')[-2]), target='downloads')
            bot.reply_to(message, "تم تحميل الفيديو من إنستغرام.")
        elif 'tiktok.com' in url:
            api = TikTokApi()
            video = api.video(url)
            video.download('downloads/tiktok_video.mp4')
            bot.reply_to(message, "تم تحميل الفيديو من تيك توك.")
        elif 'facebook.com' in url:
            # استخدم مكتبة مناسبة لتحميل الفيديوهات من فيس بوك
            bot.reply_to(message, "تطبيق دعم تحميل فيس بوك قيد التطوير.")
        else:
            bot.reply_to(message, "رابط غير مدعوم.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")

bot.polling()
