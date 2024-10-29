from aiogram import Router
from aiogram.filters.command import Command
from Instruments.CGM import full_name, categories, date
from Instruments.DB import add_new_user as anu, check_status as cs
from Instruments.Phrases import load_phrases
from Instruments.Config import admins

rs = Router()


@rs.message(Command(commands=["start", "reload", "statistics"]))
async def commands_handler(message, state):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.text == "/start":
        username = message.from_user.username
        await anu(user_id, username)
        status = await cs(user_id)
        if status:
            await categories(chat_id, state)
        else:
            await full_name(chat_id, state)

    elif message.text == "/reload":
        if str(user_id) in admins:
            await load_phrases()
            await message.answer("Контент загружен из базы данных")
        else:
            await message.answer("Эта команда предназначена только для администраторов")

    elif message.text == "/statistics":
        if str(user_id) in admins:
            await date(chat_id, state)
        else:
            await message.answer("Эта команда предназначена только для администраторов")
