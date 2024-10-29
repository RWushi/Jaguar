from Instruments.Config import user_questions, city_groups
from Instruments.DB import get_user_data as gud, get_appeal_number as ga, set_appeal_number as san
from Omnidesk.Create import create_appeal
from Omnidesk.AddMessage import add_message
from Omnidesk.CheckStatus import check_status


async def get_data(user_id, text):
    phone, username, full_name = await gud(user_id)
    help_data = user_questions[user_id]

    if len(help_data) == 1:
        city, subject = help_data[0], 'Общие вопросы'
    else:
        city, subject = help_data[:2]

    content = text
    group_id = city_groups[city]
    return phone, username, user_id, full_name, subject, content, group_id


async def check_case(chat_id, text):
    case = await ga(chat_id)

    if case:
        status, omni_id = await check_status(case)
        if status != 'closed':
            await add_message(case, text, omni_id)
            return

    user_data = await get_data(chat_id, text)
    case_number = await create_appeal(*user_data)
    await san(chat_id, case_number)
