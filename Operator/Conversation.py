from aiogram import Router
from Instruments.Config import States, user_questions, user_operator_state
from Instruments.CGM import categories, category, question_answer
from Omnidesk.Auxiliary import check_case

roc = Router()


@roc.message(States.categories_operator)
@roc.message(States.category_operator)
@roc.message(States.rate_operator)
@roc.message(States.operator)
async def text_operator_handler(message, state):
    chat_id = message.chat.id
    text = message.text

    if text == 'Вернуться назад':
        state_str = await state.get_state()
        current_state = state_str.split(':')[1].split('_')[0]

        if current_state == 'categories':
            await categories(chat_id, state)
        elif current_state == 'category':
            name = user_questions[chat_id][1]
            await category(chat_id, state, name)
        elif current_state == 'rate':
            await question_answer(chat_id, state)

        user_operator_state[chat_id] = False

    elif text == 'Позвать оператора':
        await message.answer('Вы итак находитесь в чате с оператором, напишите свое сообщение')

    else:
        await check_case(chat_id, text)
