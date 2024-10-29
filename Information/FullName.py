from aiogram import Router, F
from Instruments.Config import States
from Instruments.DB import set_full_name
from Instruments.CGM import phone

rfn = Router()


@rfn.message(F.text, States.full_name)
async def full_name_handler(message, state):
    user_id = message.from_user.id
    chat_id = message.chat.id
    full_name = message.text

    await set_full_name(user_id, full_name)
    await phone(chat_id, state)
