from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبا! أنا بوت الحماية الخاص بك.")

# دالة لعرض الأوامر
def الاوامر(update: Update, context: CallbackContext):
    commands = """
    الأوامر المتاحة:
    1. حظر [معرف المستخدم] - لحظر مستخدم
    2. طرد [معرف المستخدم] - لطرد مستخدم
    3. كتم [معرف المستخدم] - لكتم صوت مستخدم
    4. إلغاء_كتم [معرف المستخدم] - لإلغاء كتم صوت مستخدم
    5. قفل - لقفل المجموعة
    6. فتح - لفتح المجموعة
    7. قفل_الفويسات - لقفل الفويسات
    8. فتح_الفويسات - لفتح الفويسات
    9. قفل_المتحركات - لقفل المتحركات
    10. فتح_المتحركات - لفتح المتحركات
    11. قفل_السبام - لقفل السبام
    12. فتح_السبام - لفتح السبام
    13. قفل_التوجيه - لقفل التوجيه
    14. فتح_التوجيه - لفتح التوجيه
    15. قفل_الإضافة - لقفل الإضافة
    16. فتح_الإضافة - لفتح الإضافة
    17. قفل_الصور - لقفل الصور
    18. فتح_الصور - لفتح الصور
    19. قفل_التسجيل_المرئي - لقفل التسجيل المرئي
    20. فتح_التسجيل_المرئي - لفتح التسجيل المرئي
    21. منح_المميز [معرف المستخدم] - لمنح رتبة المميز لمستخدم
    22. سحب_المميز [معرف المستخدم] - لسحب رتبة المميز من مستخدم
    23. تنظيف - لحذف جميع الصور والمتحركات والملصقات
    """
    update.message.reply_text(commands)

# دالة لتنظيف المجموعة
def تنظيف(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        count = 0
        chat_id = update.message.chat.id
        
        # استرداد الرسائل
        messages = context.bot.get_chat_history(chat_id)
        
        for message in messages:
            if message.photo or message.animation or message.sticker:
                context.bot.delete_message(chat_id, message.message_id)
                count += 1
        
        update.message.reply_text(f"تم حذف {count} عنصر من الصور والمتحركات والملصقات.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لمنح رتبة المميز
def منح_المميز(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user_id = int(context.args[0])
            if user_id not in premium_users:
                premium_users.append(user_id)
                update.message.reply_text(f"تم منح المميز للمستخدم {user_id}.")
            else:
                update.message.reply_text("المستخدم لديه بالفعل رتبة المميز.")
        else:
            update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لسحب رتبة المميز
def سحب_المميز(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user_id = int(context.args[0])
            if user_id in premium_users:
                premium_users.remove(user_id)
                update.message.reply_text(f"تم سحب المميز من المستخدم {user_id}.")
            else:
                update.message.reply_text("المستخدم لا يملك رتبة المميز.")
        else:
            update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لحظر مستخدم
def حظر(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            context.bot.ban_chat_member(update.message.chat.id, user)
            update.message.reply_text(f"تم حظر {user}.")
        else:
            update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لطرد مستخدم
def طرد(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            context.bot.kick_chat_member(update.message.chat.id, user)
            update.message.reply_text(f"تم طرد {user}.")
        else:
            update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لكتم صوت مستخدم
def كتم(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            context.bot.restrict_chat_member(update.message.chat.id, user, can_send_messages=False)
            update.message.reply_text(f"تم كتم صوت {user}.")
        else:
            update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لإلغاء كتم صوت مستخدم
def إلغاء_كتم(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        if context.args:
            user = context.args[0]
            context.bot.restrict_chat_member(update.message.chat.id, user, can_send_messages=True)
            update.message.reply_text(f"تم إلغاء كتم صوت {user}.")
        else:
            update.message.reply_text("يرجى تحديد المستخدم.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الرسائل
def قفل(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        context.bot.restrict_chat_member(update.message.chat.id, update.message.from_user.id, can_send_messages=False)
        update.message.reply_text("تم قفل المجموعة.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الرسائل
def فتح(update: Update, context: CallbackContext):
    if update.message.from_user.id in admins:
        context.bot.restrict_chat_member(update.message.chat.id, update.message.from_user.id, can_send_messages=True)
        update.message.reply_text("تم فتح المجموعة.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الفويسات
def قفل_الفويسات(update: Update, context: CallbackContext):
    global block_voice
    if update.message.from_user.id in admins:
        block_voice = True
        update.message.reply_text("تم قفل الفويسات.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الفويسات
def فتح_الفويسات(update: Update, context: CallbackContext):
    global block_voice
    if update.message.from_user.id in admins:
        block_voice = False
        update.message.reply_text("تم فتح الفويسات.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل المتحركات
def قفل_المتحركات(update: Update, context: CallbackContext):
    global block_gifs
    if update.message.from_user.id in admins:
        block_gifs = True
        update.message.reply_text("تم قفل المتحركات.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح المتحركات
def فتح_المتحركات(update: Update, context: CallbackContext):
    global block_gifs
    if update.message.from_user.id in admins:
        block_gifs = False
        update.message.reply_text("تم فتح المتحركات.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل السبام
def قفل_السبام(update: Update, context: CallbackContext):
    global block_spam
    if update.message.from_user.id in admins:
        block_spam = True
        update.message.reply_text("تم قفل السبام.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح السبام
def فتح_السبام(update: Update, context: CallbackContext):
    global block_spam
    if update.message.from_user.id in admins:
        block_spam = False
        update.message.reply_text("تم فتح السبام.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل التوجيه
def قفل_التوجيه(update: Update, context: CallbackContext):
    global block_forward
    if update.message.from_user.id in admins:
        block_forward = True
        update.message.reply_text("تم قفل التوجيه.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح التوجيه
def فتح_التوجيه(update: Update, context: CallbackContext):
    global block_forward
    if update.message.from_user.id in admins:
        block_forward = False
        update.message.reply_text("تم فتح التوجيه.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الإضافة
def قفل_الإضافة(update: Update, context: CallbackContext):
    global block_add
    if update.message.from_user.id in admins:
        block_add = True
        update.message.reply_text("تم قفل الإضافة.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الإضافة
def فتح_الإضافة(update: Update, context: CallbackContext):
    global block_add
    if update.message.from_user.id in admins:
        block_add = False
        update.message.reply_text("تم فتح الإضافة.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل الصور
def قفل_الصور(update: Update, context: CallbackContext):
    global block_photos
    if update.message.from_user.id in admins:
        block_photos = True
        update.message.reply_text("تم قفل الصور.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح الصور
def فتح_الصور(update: Update, context: CallbackContext):
    global block_photos
    if update.message.from_user.id in admins:
        block_photos = False
        update.message.reply_text("تم فتح الصور.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لقفل التسجيل المرئي
def قفل_التسجيل_المرئي(update: Update, context: CallbackContext):
    global block_video
    if update.message.from_user.id in admins:
        block_video = True
        update.message.reply_text("تم قفل التسجيل المرئي.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لفتح التسجيل المرئي
def فتح_التسجيل_المرئي(update: Update, context: CallbackContext):
    global block_video
    if update.message.from_user.id in admins:
        block_video = False
        update.message.reply_text("تم فتح التسجيل المرئي.")
    else:
        update.message.reply_text("ليس لديك صلاحيات كافية.")

# دالة لمعالجة الرسائل
def check_messages(update: Update, context: CallbackContext):
    global message_count
    user_id = update.message.from_user.id
    
    # التحقق من صلاحيات المستخدم
    if user_id in premium_users:
        return  # المستخدم المميز يمكنه إرسال كل شيء

    # تطبيق قيود الرسائل
    if block_links and update.message.entities:
        for entity in update.message.entities:
            if entity.type == "url":
                update.message.delete()
                break

    if block_voice and update.message.voice:
        update.message.delete()

    if block_gifs and update.message.animation:
        update.message.delete()

    if block_photos and update.message.photo:
        update.message.delete()

    if block_video and update.message.video:
        update.message.delete()

    if block_forward and update.message.forward_from:
        update.message.delete()

    if block_add and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            context.bot.kick_chat_member(update.message.chat.id, member.id)

    if block_spam:
        text = update.message.text
        if text:
            message_count[text] = message_count.get(text, 0) + 1
            if message_count[text] > 5:
                update.message.delete()
                message_count[text] = 0  # إعادة العد بعد الحذف

# بدء البوت
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("الاوامر", الاوامر))
    dp.add_handler(CommandHandler("تنظيف", تنظيف))
    dp.add_handler(CommandHandler("منح_المميز", منح_المميز))
    dp.add_handler(CommandHandler("سحب_المميز", سحب_المميز))
    dp.add_handler(CommandHandler("حظر", حظر))
    dp.add_handler(CommandHandler("طرد", طرد))
    dp.add_handler(CommandHandler("كتم", كتم))
    dp.add_handler(CommandHandler("إلغاء_كتم", إلغاء_كتم))
    dp.add_handler(CommandHandler("قفل", قفل))
    dp.add_handler(CommandHandler("فتح", فتح))
    dp.add_handler(CommandHandler("قفل_الفويسات", قفل_الفويسات))
    dp.add_handler(CommandHandler("فتح_الفويسات", فتح_الفويسات))
    dp.add_handler(CommandHandler("قفل_المتحركات", قفل_المتحركات))
    dp.add_handler(CommandHandler("فتح_المتحركات", فتح_المتحركات))
    dp.add_handler(CommandHandler("قفل_السبام", قفل_السبام))
    dp.add_handler(CommandHandler("فتح_السبام", فتح_السبام))
    dp.add_handler(CommandHandler("قفل_التوجيه", قفل_التوجيه))
    dp.add_handler(CommandHandler("فتح_التوجيه", فتح_التوجيه))
    dp.add_handler(CommandHandler("قفل_الإضافة", قفل_الإضافة))
    dp.add_handler(CommandHandler("فتح_الإضافة", فتح_الإضافة))
    dp.add_handler(CommandHandler("قفل_الصور", قفل_الصور))
    dp.add_handler(CommandHandler("فتح_الصور", فتح_الصور))
    dp.add_handler(CommandHandler("قفل_التسجيل_المرئي", قفل_التسجيل_المرئي))
    dp.add_handler(CommandHandler("فتح_التسجيل_المرئي", فتح_التسجيل_المرئي))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_messages))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
                
