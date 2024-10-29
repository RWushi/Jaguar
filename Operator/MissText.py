from aiogram import Router, F

rot = Router()


@rot.message(F.text)
async def text_operator_handler(message):
    text = message.text

    if text == 'Позвать оператора':
        await message.answer('Чтобы позвать оператора нужно нажать на кнопку "Позвать оператора", а не отправлять такой текст')
    else:
        await message.answer('Я не понимаю такой команды, пожалуйста, нажмите кнопку')
