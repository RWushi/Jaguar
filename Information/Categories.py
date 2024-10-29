from aiogram import Router
from Instruments.Config import States, user_questions
from Instruments.CGM import category, call_operator

rca = Router()


@rca.callback_query(States.choose_category)
async def categories_handler(callback, state):
    await callback.message.delete()
    choice = callback.data
    chat_id = callback.message.chat.id

    if choice == 'operator':
        await call_operator(chat_id, state)

    else:
        if len(user_questions[chat_id]) < 2:
            user_questions[chat_id].append(choice)
        else:
            user_questions[chat_id][1] = choice
        await category(chat_id, state, callback.data)
