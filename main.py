#By @N0040
#Channel @B3kkk

import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

app = Client("What-@B3KKK",
api_id=14170449, 
api_hash="03488b3c030fe095667e7ca22fe34954", 
bot_token="7218686976:AAEUzTUoUBQsohKwDRM8-mMwcX24Cw4GrOk")


@app.on_message(filters.command("start") & filters.private)
def start(client, message):
    message.reply(f"Hello {message.from_user.mention} !\n› This bot is made to download from any site \n› Just send URL", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Source Channel", url="t.me/B3KKK")]]))
@app.on_message(filters.text & filters.private)
async def download(client, message):
     EnyWeb = message.text 
     Me = message.from_user.mention
     x = await message.reply("🔍 Searching....")
     try:
       url='https://ssyoutube.com/api/convert'
       head={
'user_agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',}
       data={'url':EnyWeb,}
       req=requests.post(url,headers=head,data=data).json()
       Media=req['url'][0]['url']
     except Exception as e:
        await x.delete()
        print(e)
        return await message.reply("› Invaild URL")
     try:
        caption = f"**Done By {Me}**"
        await message.reply_audio(
             Media,
             caption=caption
        )
        await x.delete()
     except Exception as e:
        print(e)
        await x.delete()
        return await message.reply("An error !")

print("Wait........")
app.run()
print("Bot is run")
    
#By @N0040
#Channel @B3kkk  
