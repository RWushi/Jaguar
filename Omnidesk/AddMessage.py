from Instruments.Config import subdomain, headers
import aiohttp

pre_url = f"https://{subdomain}.omnidesk.ru/api/cases/"


async def add_message(case_number, text, omni_id):
    async with aiohttp.ClientSession() as session:
        url_status = f"{pre_url}{case_number}.json"
        body_status = {"case": {"status": 'open'}}
        await session.put(url_status, headers=headers, json=body_status)

        url_message = f"{pre_url}{case_number}/messages.json"
        body_message = {"message": {"content": text, "user_id": omni_id}}
        await session.post(url_message, headers=headers, json=body_message)
