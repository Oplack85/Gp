#By Team Aljoker For You ❤️🤡

from telethon import TelegramClient, events, Button
import subprocess
from random import choices, randint

api_id = 23970174
api_hash = 'f1db2e38b2c73448ef09c504187e888d'
bot_token = '7218686976:AAHbE6XlKHaiqW-GK8e-2LFPwCt_4Het-jc'

Hussein = TelegramClient('aljoker_session', api_id, api_hash).start(bot_token=bot_token)

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

        create_user_aljoker = f'sudo su - postgres -c "psql -c \\"CREATE USER joker{OHussein} WITH PASSWORD \'joker{OHussein}\';\\""'
        create_db_aljoker = f'sudo su - postgres bash -c "createdb joker{OHussein} -O joker{OHussein}"'

        create_user_process = subprocess.Popen(create_user_aljoker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        user_res, user_err = create_user_process.communicate()

        if 'CREATE ROLE' in user_res.decode():
            create_db_process = subprocess.Popen(create_db_aljoker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            db_res, db_err = create_db_process.communicate()

            if not db_err:
                await event.respond(f'''**وهاي قاعدة البيانات وتدلل علينا 😘 : `postgresql://joker{OHussein}:joker{OHussein}@localhost:5432/joker{OHussein}`**''')
            else:
                await event.respond(f'حدث خطأ أثناء إنشاء قاعدة البيانات:\n{db_err.decode()}')
        else:
            await event.respond(f'حدث خطأ أثناء إنشاء المستخدم:\n{user_err.decode()}')

print("البوت يشتغل استمتع 😍...")
Hussein.run_until_disconnected()
