from aiogram import Router
from Instruments.Config import States, user_questions
from Instruments.DB import set_city
from Instruments.CGM import confirmation

rc = Router()


@rc.callback_query(States.cities)
async def cities_handler(callback, state):
    await callback.message.delete()
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    city = callback.data

    user_questions[user_id] = [city]
    await set_city(user_id, city)
    await confirmation(chat_id, state, city)

