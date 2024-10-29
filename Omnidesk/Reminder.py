from aiogram import Router
from Instruments.DB import get_appeal_number as gan
from Omnidesk.ChangeStatus import update_status
from Instruments.Config import States
from Instruments.CGM import send_missed_messages

rr = Router()


@rr.callback_query()
async def reminder_handler(callback, state):
    message = callback.message
    await message.delete()
    choice = callback.data
    chat_id = message.chat.id
    case_number = await gan(chat_id)

    if choice == 'not_good':
        await update_status(case_number, 'open')
        await message.answer('Оператор скоро подключится к чату')
        await state.set_state(States.operator)
        await send_missed_messages(chat_id)

    elif choice == 'good':
        await update_status(case_number, 'closed')
        await message.answer('Я очень рад, что мой ответ помог! Желаю Вам успехов!')
