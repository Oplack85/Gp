import psycopg2
import uuid

api_id = 23970174  # استبدل بـ API ID الخاص بك
api_hash = 'f1db2e38b2c73448ef09c504187e888d'  # استبدل بـ API Hash الخاص بك
bot_token = '7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc'  # استبدل بـ توكن البوت الخاص بك

Hussein = TelegramClient('aljoker_session', api_id, api_hash).start(bot_token=bot_token)

# إعداد الاتصال بقاعدة البيانات
def create_db_connection():
    return psycopg2.connect(
        dbname="data_cbun",  # استبدل باسم قاعدة البيانات
        user="data_cbun_user",    # استبدل باسم المستخدم
        password="vONvqIraGuQdH2OZQaGrHYzUHoLPTlP6", # استبدل بكلمة المرور
        host="dpg-crk80bjqf0us73df2ds0-a",        # استبدل بعنوان المضيف
        port="5432"              # عادةً ما يكون 5432
    )

@Hussein.on(events.NewMessage(pattern='/start'))
async def aljoker(event):
    keyboard = [[Button.inline('إنشاء قاعدة بيانات', b'aljoker_postgres')]]
    await event.reply(
        f'''**اهلاً وسهلاً حبيبي {event.sender.first_name}،
‎لإنشاء قاعدة بيانات خاصة بسورس الجوكر قم بالضغط على زر إنشاء قاعدة بيانات**''',
        buttons=keyboard
    )

@Hussein.on(events.CallbackQuery)
async def handle_callback(event):
    if event.data == b'aljoker_postgres':
        OHussein = ''.join(choices('abcdefghijklmnopqrstuvwxyz0123456789', k=randint(5, 10)))
        await event.respond('**᯽︙ انتظرني أسوي لك قاعدة بيانات لعيونك🥰**')

        try:
            conn = create_db_connection()
            cursor = conn.cursor()

            # إنشاء المستخدم
            create_user_query = f"CREATE USER joker{OHussein} WITH PASSWORD 'joker{OHussein}';"
            cursor.execute(create_user_query)

            # إنشاء قاعدة البيانات
            create_db_query = f"CREATE DATABASE joker{OHussein} OWNER joker{OHussein};"
            cursor.execute(create_db_query)

            conn.commit()
            await event.respond(f'''**وهاي قاعدة البيانات وتدلل علينا 😘 : `postgresql://joker{OHussein}:joker{OHussein}@{your_host}:5432/joker{OHussein}`**''')
        except Exception as e:
            await event.respond(f'حدث خطأ أثناء إنشاء المستخدم أو قاعدة البيانات:\n{str(e)}')
        finally:
            cursor.close()
            conn.close()

print("البوت يشتغل استمتع 😍...")
Hussein.run_until_disconnected()
