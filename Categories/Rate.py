from aiogram import Router
from Instruments.Config import States, user_questions, reasons_list
from Instruments.DB import operator_click
from Instruments.CGM import call_operator, category
from Omnidesk.Auxiliary import check_case

rcr = Router()

operator_text = 'Я хочу сменить инструктора по причине: '


@rcr.callback_query(States.rate)
async def rate_handler(callback, state):
    await callback.message.delete()
    choice = callback.data
    chat_id = callback.message.chat.id

    if choice == 'operator':
        city, section, number = user_questions[chat_id]
        await operator_click(city, section, number)
        await call_operator(chat_id, state)

    elif choice == 'ok':
        await callback.message.answer('Я очень рад, что мой ответ помог! Желаю Вам успехов!')

    elif choice == 'back':
        category_name = user_questions[chat_id][1]
        await category(chat_id, state, category_name)

    else: #Если пользователь выбирает причину смены инструктора
        await call_operator(chat_id, state, True)
        text = f'{operator_text}{reasons_list[int(choice)-1]}'
        await check_case(chat_id, text)
