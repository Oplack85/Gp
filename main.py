from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
)

# استبدل 'YOUR_TOKEN' برمز التوكن الخاص بك
TOKEN = '7218686976:AAEUzTUoUBQsohKwDRM8-mMwcX24Cw4GrOk'

# قائمة لحفظ المشرفين والمميزين
admins = []
premium_users = []

# متغيرات لحفظ الحالات
block_links = False
block_voice = False
block_gifs = False
block_photos = False
block_video = False
block_spam = False
block_forward = False
block_add = False
message_count = {}

# دالة لبدء البوت
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("مرحبا! أنا بوت الحماية الخاص بك.")

# دالة لعرض الأوامر
async def commands(update: Update, context: CallbackContext):
    commands_text = """
    الأوامر المتاحة:
    /start - بدء البوت
    /commands - عرض الأوامر
    /تنظيف - تنظيف المجموعة
    /منح_المميز [معرف المستخدم] - منح رتبة المميز
    /سحب_المميز [معرف المستخدم] - سحب رتبة المميز
    /حظر [معرف المستخدم] - حظر مستخدم
    /طرد [معرف المستخدم] - طرد مستخدم
    /كتم [معرف المستخدم] - كتم صوت مستخدم
    /إلغاء_كتم [معرف المستخدم] - إلغاء كتم صوت مستخدم
    /قفل - قفل المجموعة
    /فتح - فتح المجموعة
    /قفل_الفويسات - قفل الفويسات
    /فتح_الفويسات - فتح الفويسات
    /قفل_المتحركات - قفل المتحركات
    /فتح_المتحركات - فتح المتحركات
    /قفل_السبام - قفل السبام
    /فتح_السبام - فتح السبام
    /قفل_التوجيه - قفل التوجيه
    /فتح_التوجيه - فتح التوجيه
    /قفل_الإضافة - قفل الإضافة
    /فتح_الإضافة - فتح الإضافة
    /قفل_الصور - قفل الصور
    /فتح_الصور - فتح الصور
    /قفل_التسجيل_المرئي - قفل التسجيل المرئي
    /فتح_التسجيل_المرئي - فتح التسجيل المرئي
    """
    await update.message.reply_text(commands_text)

# دالة لتنظيف المجموعة
async def تنظيف(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        count = 0
        chat_id = update.message.chat.id
        
        # استرداد الرسائل
        messages = await context.bot.get_chat_history(chat_id)
        
        for message in messages:
            if message.photo or message.animation or message.sticker:
                await context.bot.delete_message(chat_id, message.message_id)
                count += 1
        
        await update.message.reply_text(f"تم حذف {count} عنصر من الصور والمتحركات والملصقات.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لمنح رتبة المميز
async def منح_المميز(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user_id = int(context.args[0])
            if user_id not in premium_users:
                premium_users.append(user_id)
                await update.message.reply_text(f"تم منح المميز للمستخدم {user_id}.")
            else:
                await update.message.reply_text("المستخدم لديه بالفعل رتبة المميز.")
        else:
            await update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لسحب رتبة المميز
async def سحب_المميز(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user_id = int(context.args[0])
            if user_id in premium_users:
                premium_users.remove(user_id)
                await update.message.reply_text(f"تم سحب المميز من المستخدم {user_id}.")
            else:
                await update.message.reply_text("المستخدم لا يملك رتبة المميز.")
        else:
            await update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لحظر مستخدم
async def حظر(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            await context.bot.ban_chat_member(update.message.chat.id, user)
            await update.message.reply_text(f"تم حظر {user}.")
        else:
            await update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لطرد مستخدم
async def طرد(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            await context.bot.kick_chat_member(update.message.chat.id, user)
            await update.message.reply_text(f"تم طرد {user}.")
        else:
            await update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لكتم صوت مستخدم
async def كتم(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            await context.bot.restrict_chat_member(update.message.chat.id, user, can_send_messages=False)
            await update.message.reply_text(f"تم كتم صوت {user}.")
        else:
            await update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لإلغاء كتم صوت مستخدم
async def إلغاء_كتم(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            await context.bot.restrict_chat_member(update.message.chat.id, user, can_send_messages=True)
            await update.message.reply_text(f"تم إلغاء كتم صوت {user}.")
        else:
            await update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الرسائل
async def قفل(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        await context.bot.restrict_chat_member(update.message.chat.id, update.message.from_user.id, can_send_messages=False)
        await update.message.reply_text("تم قفل المجموعة.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الرسائل
async def فتح(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        await context.bot.restrict_chat_member(update.message.chat.id, update.message.from_user.id, can_send_messages=True)
        await update.message.reply_text("تم فتح المجموعة.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الفويسات
async def قفل_الفويسات(update: Update, context: CallbackContext):
    global block_voice
    if update.message.from_user.id in admins:
        block_voice = True
        await update.message.reply_text("تم قفل الفويسات.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الفويسات
async def فتح_الفويسات(update: Update, context: CallbackContext):
    global block_voice
    if update.message.from_user.id in admins:
        block_voice = False
        await update.message.reply_text("تم فتح الفويسات.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل المتحركات
async def قفل_المتحركات(update: Update, context: CallbackContext):
    global block_gifs
    if update.message.from_user.id in admins:
        block_gifs = True
        await update.message.reply_text("تم قفل المتحركات.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح المتحركات
async def فتح_المتحركات(update: Update, context: CallbackContext):
    global block_gifs
    if update.message.from_user.id in admins:
        block_gifs = False
        await update.message.reply_text("تم فتح المتحركات.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل السبام
async def قفل_السبام(update: Update, context: CallbackContext):
    global block_spam
    if update.message.from_user.id in admins:
        block_spam = True
        await update.message.reply_text("تم قفل السبام.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح السبام
async def فتح_السبام(update: Update, context: CallbackContext):
    global block_spam
    if update.message.from_user.id in admins:
        block_spam = False
        await update.message.reply_text("تم فتح السبام.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل التوجيه
async def قفل_التوجيه(update: Update, context: CallbackContext):
    global block_forward
    if update.message.from_user.id in admins:
        block_forward = True
        await update.message.reply_text("تم قفل التوجيه.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح التوجيه
async def فتح_التوجيه(update: Update, context: CallbackContext):
    global block_forward
    if update.message.from_user.id in admins:
        block_forward = False
        await update.message.reply_text("تم فتح التوجيه.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الإضافة
async def قفل_الإضافة(update: Update, context: CallbackContext):
    global block_add
    if update.message.from_user.id in admins:
        block_add = True
        await update.message.reply_text("تم قفل الإضافة.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الإضافة
async def فتح_الإضافة(update: Update, context: CallbackContext):
    global block_add
    if update.message.from_user.id in admins:
        block_add = False
        await update.message.reply_text("تم فتح الإضافة.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الصور
async def قفل_الصور(update: Update, context: CallbackContext):
    global block_photos
    if update.message.from_user.id in admins:
        block_photos = True
        await update.message.reply_text("تم قفل الصور.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الصور
async def فتح_الصور(update: Update, context: CallbackContext):
    global block_photos
    if update.message.from_user.id in admins:
        block_photos = False
        await update.message.reply_text("تم فتح الصور.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الفيديو
async def قفل_التسجيل_المرئي(update: Update, context: CallbackContext):
    global block_video
    if update.message.from_user.id in admins:
        block_video = True
        await update.message.reply_text("تم قفل التسجيل المرئي.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الفيديو
async def فتح_التسجيل_المرئي(update: Update, context: CallbackContext):
    global block_video
    if update.message.from_user.id in admins:
        block_video = False
        await update.message.reply_text("تم فتح التسجيل المرئي.")
    else:
        await update.message.reply_text("ليس لديك صلاحيات كافية.")

# بدء البوت
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("commands", commands))  # تغيير هنا
    app.add_handler(CommandHandler("تنظيف", تنظيف))
    app.add_handler(CommandHandler("منح_المميز", منح_المميز))
    app.add_handler(CommandHandler("سحب_المميز", سحب_المميز))
    app.add_handler(CommandHandler("حظر", حظر))
    app.add_handler(CommandHandler("طرد", طرد))
    app.add_handler(CommandHandler("كتم", كتم))
    app.add_handler(CommandHandler("إلغاء_كتم", إلغاء_كتم))
    app.add_handler(CommandHandler("قفل", قفل))
    app.add_handler(CommandHandler("فتح", فتح))
    app.add_handler(CommandHandler("قفل_الفويسات", قفل_الفويسات))
    app.add_handler(CommandHandler("فتح_الفويسات", فتح_الفويسات))
    app.add_handler(CommandHandler("قفل_المتحركات", قفل_المتحركات))
    app.add_handler(CommandHandler("فتح_المتحركات", فتح_المتحركات))
    app.add_handler(CommandHandler("قفل_السبام", قفل_السبام))
    app.add_handler(CommandHandler("فتح_السبام", فتح_السبام))
    app.add_handler(CommandHandler("قفل_التوجيه", قفل_التوجيه))
    app.add_handler(CommandHandler("فتح_التوجيه", فتح_التوجيه))
    app.add_handler(CommandHandler("قفل_الإضافة", قفل_الإضافة))
    app.add_handler(CommandHandler("فتح_الإضافة", فتح_الإضافة))
    app.add_handler(CommandHandler("قفل_الصور", قفل_الصور))
    app.add_handler(CommandHandler("فتح_الصور", فتح_الصور))
    app.add_handler(CommandHandler("قفل_التسجيل_المرئي", قفل_التسجيل_المرئي))
    app.add_handler(CommandHandler("فتح_التسجيل_المرئي", فتح_التسجيل_المرئي))

    await app.start_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
            
