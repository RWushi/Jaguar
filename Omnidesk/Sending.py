from Instruments.Config import bot, user_operator_state, operators_messages


async def send_operators_message(user_id, text):
    if user_operator_state[user_id]:
        await bot.send_message(user_id, text)
    else:
        operators_messages.setdefault(user_id, []).append(text)
