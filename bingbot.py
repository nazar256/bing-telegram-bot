import asyncio
import os
import re

from telebot.async_telebot import AsyncTeleBot

from EdgeGPT import Chatbot

# Insert your Bot token
with open(os.getenv('BOT_TOKEN_FILE'), 'r') as file:
    BOT_TOKEN = file.read()
bot = AsyncTeleBot(BOT_TOKEN)
style = os.getenv('CONVERSATION_STYLE_TYPE')

# Add your telegram id to the list without @ symbol
authorized_id = os.getenv('AUTHORIZED_IDS').split(",")


async def bingChat(prompt, is_ref=False):
    # Update your cookies.json path here
    gbot = Chatbot(cookiePath=os.getenv('COOKIE_FILE'))
    response_dict = await gbot.ask(prompt=prompt, )
    if is_ref:
        return response_dict['item']['messages'][1]["adaptiveCards"][0]["body"][0]["text"]
    return re.sub(r'\[\^\d\^\]', '', response_dict['item']['messages'][1]['text'])


@bot.message_handler(commands=['ask'])
async def ask(message, is_ref=False):
    try:
        username = message.from_user.username
        if username not in authorized_id:
            await bot.reply_to(message, "Not authorized to use this bot")
            return
        prompt = message.text.replace("/ask", "")
        print(f"Request received from {username} - {message.text}")
        if not prompt:
            await bot.reply_to(message, "Empty query sent. Add your query /ask <message>")
        else:
            bot_response = await bingChat(prompt, is_ref)
            print(f"Response received - {bot_response}")
            await bot.reply_to(message, bot_response.replace('?\n\n', ''))
    except Exception as e:
        print("Exception happened")
        print(e)


@bot.message_handler(commands=['askref'])
async def askref(message):
    await ask(message, is_ref=True)


@bot.message_handler(commands=['start'])
async def start(message):
    try:
        username = message.from_user.username
        result = f"""
        Welcome {username}!!
        """
        await bot.send_message(message.chat.id, result)
    except Exception as e:
        print("Exception happened")
        print(e)

@bot.message_handler(func=lambda m: True)
async def input(message):
    await ask(message)

async def main():
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(main())