import aiohttp
import json

async def send_request(data):
    url = 'https://telegramwh.omnidesk.ru/webhooks/telegram/5110/98b40bf661687a93'
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data), headers=headers) as response:
            if response.content_length:
                result = await response.json()
            else:
                result = None

            if result and result.get('success') == '2':
                return False
            elif result and result.get('success'):
                print("Запрос отправлен")
                return True


async def get_data(user_id, chat_id, text):
    full_name, username = await gud(user_id)

    if ' ' in full_name:
        first, last = full_name.split()[:2]
    else:
        first = full_name; last = None

    return { "message" : {
            "text": text,
            "chat": {
                "id": chat_id,
                "first_name": first,
                "last_name": last },
            "from": {
                "id": user_id,
                "first_name": first,
                "username": username }}}
