import random
import string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess

def run_command(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

def generate_random_string(length: int) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = generate_random_string(8)       # توليد اسم مستخدم عشوائي
    password = generate_random_string(12)   # توليد كلمة مرور عشوائية
    database = generate_random_string(10)   # توليد اسم قاعدة بيانات عشوائية
    db_file = generate_random_string(8)     # توليد اسم ملف قاعدة بيانات عشوائي
    db_folder = generate_random_string(10)   # توليد اسم مجلد عشوائي

    commands = [
        f"mkdir -p $PREFIX/var/lib/postgresql/{db_folder}",
        f"initdb $PREFIX/var/lib/postgresql/{db_folder}",
        f"pg_ctl -D $PREFIX/var/lib/postgresql/{db_folder} start",
        f"createuser --superuser {user}",
        f"psql -U postgres -d postgres -c \"ALTER USER {user} WITH PASSWORD '{password}';\"",
        f"psql -U postgres -d postgres -c \"CREATE DATABASE {database} OWNER {user};\"",
        f"pg_dump {database} > $PREFIX/var/lib/postgresql/{db_folder}/{db_file}.sql",
        f"pg_ctl -D $PREFIX/var/lib/postgresql/{db_folder} status"
    ]
    
    responses = []
    for command in commands:
        response = run_command(command)
        responses.append(response)

    connection_string = f"postgresql://{user}:{password}@localhost:5432/{database}"
    
    await update.message.reply_text(f"Connection String: {connection_string}\n\nResponses:\n" + "\n".join(responses))

def main():
    application = ApplicationBuilder().token("7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc").build()

    application.add_handler(CommandHandler("setup", setup))

    application.run_polling()

if __name__ == '__main__':
    main()
