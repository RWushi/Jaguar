from aiogram import Router
from Instruments.CGM import question_answer, call_operator, categories
from Instruments.DB import question_click
from Instruments.Config import States, user_questions
from Instruments.Phrases import get_answer, get_question
from Omnidesk.Auxiliary import check_case

rcc = Router()


@rcc.callback_query(States.medical)
@rcc.callback_query(States.driving)
@rcc.callback_query(States.theory)
@rcc.callback_query(States.internal_exam)
@rcc.callback_query(States.gibdd_exam)
@rcc.callback_query(States.payment)
async def categories_handler(callback, state):
    await callback.message.delete()
    choice = callback.data
    chat_id = callback.message.chat.id

    if choice.isdigit():
        if len(user_questions[chat_id]) < 3:
            user_questions[chat_id].append(int(choice))
        else:
            user_questions[chat_id][2] = int(choice)

        city, category = user_questions[chat_id][:2]
        await question_click(city, category, int(choice))

        state_str = await state.get_state()
        current_state = state_str.split(':')[1]

        if current_state == 'payment' or (current_state == 'gibdd_exam' and (choice == '1' or
                                        (choice == '3' and city == 'Воронеж'))):
            await call_operator(chat_id, state, True)
            text = await get_question(city, category, int(choice))
            await check_case(chat_id, text)

        else:
            await question_answer(chat_id, state)

    elif choice == 'operator':
        await call_operator(chat_id, state)

    elif choice == 'back':
        await categories(chat_id, state)
