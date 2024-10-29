from .Keyboards import (cities_kb, confirmation_kb, categories_kb, questions,
                        operator_kb, reply_kb)
from .Config import (bot, States, user_questions, categories_ru_en,
                     user_operator_state, operators_messages, reasons_list)
from .DB import get_full_name, get_phone
from .Phrases import get_questions, get_answer
import re

reason_text = 'Укажите, по какой причине Вы хотите сменить инструктора?'.lower()
operator_text = 'Введите сообщение для оператора, если Вы хотите закончить диалог, нажмите \"Вернуться назад\" внизу.\n\n⚠️Внимание⚠️: Если Вы вернетесь назад, Вы больше не будете получать сообщения от оператора.\nЧтобы получить все пропущенные сообщения, снова зайдите в этот раздел.'
operator_text_auto = 'Перевожу обращение на оператора. Специалист уже спешит к Вам на помощь. Пожалуйста, дождитесь его подключения.'


async def date(chat_id, state):
    text = 'Введите начальный и конечный срок в формате ГГГГ-ММ-ДД через пробел или запятую. Например: 2024-01-01, 2024-12-31.'
    await bot.send_message(chat_id, text)
    await state.set_state(States.date)


async def full_name(chat_id, state):
    text = ("Добрый день! Спасибо, что выбрали автошколу Ягуар🚘\n"
        "Вам у нас точно понравится⭐️\n"
        "Пожалуйста, напишите свое полное ФИО")
    await bot.send_message(chat_id, text)
    await state.set_state(States.full_name)


async def phone(chat_id, state):
    text = "Теперь введите свой номер телефона в формате +7ХХХХХХХХХХ"
    await bot.send_message(chat_id, text)
    await state.set_state(States.phone)


async def city(chat_id, state):
    text = "В каком городе Вы проходите обучение?"
    await bot.send_message(chat_id, text, reply_markup=cities_kb)
    await state.set_state(States.cities)


async def confirmation(chat_id, state, town):
    fn = await get_full_name(chat_id)
    phone_num = await get_phone(chat_id)
    text = (f"Ваше ФИО: {fn}\n"
            f"Ваш номер телефона: {phone_num}\n"
            f"Ваш город: {town}\n\n"
            "Пожалуйста, удостоверьтесь, что вы правильно выбрали регион. В случае, если город "
            "выбран неверно, отменить это действие будет невозможно и мы не сможем оказывать "
            "Вам актуальную консультацию во время обучения.")
    await bot.send_message(chat_id, text, reply_markup=confirmation_kb)
    await state.set_state(States.confirmation)


async def categories(chat_id, state, repeat=False):
    fn = await get_full_name(chat_id)
    if repeat:
        text = "Выберите раздел, которого касается Ваш вопрос:"
    else:
        text = f"Добрый день, {fn}! Выберите раздел, которого касается Ваш вопрос:"
    await bot.send_message(chat_id, text, reply_markup=categories_kb)
    await state.set_state(States.choose_category)


async def category(chat_id, state, name):
    town = user_questions[chat_id][0]
    add_text, num = await get_questions(town, name)
    text = "Нажмите на цифру, соответствующую Вашему вопросу:\n\n" + add_text
    kb = await questions(num)
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(getattr(States, categories_ru_en[name]))


async def call_operator(chat_id, state, auto=False):
    state_str = await state.get_state()
    current_state = state_str.split(':')[1]

    if current_state in ('medical', 'driving', 'theory', 'internal_exam', 'gibdd_exam', 'payment'):
        current_state = 'category'
    elif current_state == 'choose_category':
        current_state = 'categories'

    necessary_state = f'{current_state}_operator'
    kb = operator_kb

    text = operator_text_auto if auto else operator_text

    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(getattr(States, necessary_state))

    user_operator_state[chat_id] = True
    await send_missed_messages(chat_id)


async def send_missed_messages(user_id):
    if user_id in operators_messages:
        for message in operators_messages[user_id]:
            await bot.send_message(user_id, f'Пропущенное сообщение от оператора:\n{message}')


async def question_answer(chat_id, state):
    town, category_str, number = user_questions[chat_id]
    text = await get_answer(town, category_str, number)
    if reason_text in text.lower():
        reasons_list_unfiltered = re.findall(r'\d+\)\s*[^.]+', text)
        for i, reason in enumerate(reasons_list_unfiltered, start=1):
            reasons_list.append(reason.replace(f"{i}) ", ""))
        kb = await questions(len(reasons_list), True)
    else:
        kb = reply_kb
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(States.rate)
