from aiogram import Router, F
from Instruments.Config import States
from Instruments.DB import set_phone
from Instruments.CGM import city

rp = Router()


@rp.message(F.text, States.phone)
async def phone_handler(message, state):
    user_id = message.from_user.id
    chat_id = message.chat.id
    phone = message.text

    await set_phone(user_id, phone)
    await city(chat_id, state)
