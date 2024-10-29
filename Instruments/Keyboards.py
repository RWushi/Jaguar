from aiogram.types import (InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb,
                           ReplyKeyboardMarkup as rkm, KeyboardButton as rkb)
from aiogram.utils.keyboard import InlineKeyboardBuilder

cities_kb = ikm(inline_keyboard=[
    [ikb(text="Воронеж", callback_data="Воронеж")],
    [ikb(text="Москва", callback_data="Москва")],
    [ikb(text="Санкт-Петербург", callback_data="Санкт-Петербург")]])

confirmation_kb = ikm(inline_keyboard=[
    [ikb(text="Все верно", callback_data="yes")],
    [ikb(text="Хочу исправить", callback_data="no")]])

categories_kb = ikm(inline_keyboard=[
    [ikb(text="Медицинская справка", callback_data="Медицинская справка")],
    [ikb(text="Вождение", callback_data="Вождение")],
    [ikb(text="Теория", callback_data="Теория")],
    [ikb(text="Внутренние экзамены", callback_data="Внутренние экзамены")],
    [ikb(text="Экзамен в ГИБДД", callback_data="Экзамен в ГИБДД")],
    [ikb(text="Оплата услуг", callback_data="Оплата услуг")],
    [ikb(text="Другой вопрос", callback_data="operator")]])


async def questions(num, reason=False):
    kb = InlineKeyboardBuilder()
    for i in range(1, num + 1):
        kb.add(ikb(text=str(i), callback_data=str(i)))

    if not reason:
        kb.add(ikb(text="Позвать оператора", callback_data="operator"))
    kb.add(ikb(text="Вернуться назад", callback_data="back"))
    kb.adjust(1)
    return kb.as_markup()


operator_kb = rkm(keyboard=[
    [rkb(text="Вернуться назад")]], resize_keyboard=True)

reply_kb = ikm(inline_keyboard=[
    [ikb(text="Позвать оператора", callback_data="operator")],
    [ikb(text="Спасибо, помогло", callback_data="ok")],
    [ikb(text="Вернуться назад", callback_data="back")]])

reminder_kb = ikm(inline_keyboard=[
    [ikb(text="Спасибо, помогло", callback_data="good")],
    [ikb(text="Еще вопросы", callback_data="not_good")]])
