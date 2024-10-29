from Instruments.Config import subdomain, headers, channel
import aiohttp

url = f"https://{subdomain}.omnidesk.ru/api/cases.json"


async def create_appeal(phone, username, user_id, full_name, subject, content, group_id):
    body = {
        "case": {
            "user_phone": phone,
            "user_telegram_data": username,
            "user_custom_id": user_id,
            "user_full_name": full_name,
            "subject": subject,
            "content": content,
            "group_id": group_id,
            "channel": channel}}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            data = await response.json()
            return data['case']['case_number']
