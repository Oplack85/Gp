import os
import random
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# استخدم مسارًا مخصصًا في Render
DB_DIR = '/app/db_files'  # مسار قاعدة البيانات
OUTPUT_FILE = '/app/db_details.txt'  # مسار ملف التفاصيل

def start_database():
    os.makedirs(DB_DIR, exist_ok=True)
    subprocess.run(["initdb", DB_DIR])
    subprocess.run(["pg_ctl", "-D", DB_DIR, "start"])

async def create_databases(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_database()
    # Clear the previous file if it exists
    with open(OUTPUT_FILE, 'w') as f:
        pass
    
    for _ in range(5):  # Create 5 databases
        random_number = random.randint(0, 9999)
        new_db_name = f"ScorpionDatas{random_number}"
        new_user = "DataScoR"
        new_password = f"Scorpass{random_number}"

        # Create the database and user
        subprocess.run(["psql", "-U", "postgres", "-d", "postgres", "-c", f"CREATE DATABASE {new_db_name} OWNER {new_user};"])
        subprocess.run(["psql", "-U", "postgres", "-d", "postgres", "-c", f"CREATE USER {new_user} WITH PASSWORD '{new_password}';"])

        # Save connection details to the file
        with open(OUTPUT_FILE, 'a') as f:
            f.write(f"postgresql://{new_user}:{new_password}@localhost:5432/{new_db_name}\n")

    await update.message.reply_text(f"5 new databases have been created. Check the details in the file: {OUTPUT_FILE}")

async def main() -> None:
    application = ApplicationBuilder().token("YOUR_TOKEN").build()

    application.add_handler(CommandHandler("data", create_databases))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    
