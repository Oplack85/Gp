import pytgpt.phind

bot = pytgpt.phind.PHIND()

def gpt(message):
    return bot.chat(f'{message}')


