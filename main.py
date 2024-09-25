import random
import string
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import subprocess

def run_command(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def generate_random_string(length: int) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def setup(update: Update, context: CallbackContext) -> None:
    user = generate_random_string(8)       # توليد اسم مستخدم عشوائي
    password = generate_random_string(12)   # توليد كلمة مرور عشوائية
    database = generate_random_string(10)   # توليد اسم قاعدة بيانات عشوائية
    db_file = generate_random_string(8)     # توليد اسم ملف قاعدة بيانات عشوائي
    db_folder = generate_random_string(10)   # توليد اسم مجلد عشوائي

    commands = [
        f"mkdir -p $PREFIX/var/lib/postgresql/{db_folder}",  # مجلد عشوائي
        f"initdb $PREFIX/var/lib/postgresql/{db_folder}",     # تهيئة قاعدة البيانات
        f"pg_ctl -D $PREFIX/var/lib/postgresql/{db_folder} start",  # بدء قاعدة البيانات
        f"createuser --superuser {user}",
        f"psql -U postgres -d postgres -c \"ALTER USER {user} WITH PASSWORD '{password}';\"",
        f"psql -U postgres -d postgres -c \"CREATE DATABASE {database} OWNER {user};\"",
        f"pg_dump {database} > $PREFIX/var/lib/postgresql/{db_folder}/{db_file}.sql",  # تصدير قاعدة البيانات إلى ملف
        f"pg_ctl -D $PREFIX/var/lib/postgresql/{db_folder} status"
    ]
    
    responses = []
    for command in commands:
        response = run_command(command)
        responses.append(response)

    # إعداد تفاصيل الاتصال بقاعدة البيانات
    connection_string = f"postgresql://{user}:{password}@localhost:5432/{database}"
    
    update.message.reply_text(f"Connection String: {connection_string}\n\nResponses:\n" + "\n".join(responses))

def main():
    updater = Updater("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc")

    updater.dispatcher.add_handler(CommandHandler("setup", setup))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
