from aiogram import Router
from Instruments.Config import States
from Instruments.DB import confirm_status
from Instruments.CGM import categories, full_name

rco = Router()


@rco.callback_query(States.confirmation)
async def confirmation_handler(callback, state):
    await callback.message.delete()
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    choice = callback.data

    if choice == 'yes':
        await confirm_status(user_id)
        await categories(chat_id, state)
    elif choice == 'no':
        await full_name(chat_id, state)
