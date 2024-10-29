from aiogram import Router, F
from Instruments.Config import States
from Statistics.Statistics import excel_report
from aiogram.types import FSInputFile
import re
from datetime import datetime

rd = Router()


@rd.message(F.text, States.date)
async def date_handler(message):
    pattern = r'(\d{4}-\d{2}-\d{2})\s*[, ]\s*(\d{4}-\d{2}-\d{2})\.?'
    match = re.search(pattern, message.text)

    if match:
        start = match.group(1)
        end = match.group(2)

        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        today = datetime.today()

        if start_date > today or end_date > today:
            await message.answer('Вы ввели будущее время')

        else:
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            await message.answer('Ваш файл готовится, подождите...')

            await excel_report(start_date, end_date)
            document = FSInputFile('Statistics/Статистика.xlsx')
            await message.answer_document(document)

    else:
        await message.answer('Не удалось распознать даты')
