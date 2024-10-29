from Instruments.Config import bot, subdomain, headers, reminder_cases
from Instruments.Keyboards import reminder_kb
import aiohttp
import asyncio

pre_url = f"https://{subdomain}.omnidesk.ru/api/cases/"
text = 'Скажите, у Вас остались еще вопросы?'


async def reminder(user_id, case_id):
    await asyncio.sleep(3600)
    status = await check_status(case_id)
    if status == 'waiting' and case_id not in reminder_cases:
        await bot.send_message(user_id, text, reply_markup=reminder_kb)
        reminder_cases.append(case_id)


async def check_status(case_id):
    url = f"{pre_url}{case_id}.json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data['case']['status']
        