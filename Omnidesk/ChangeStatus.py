from Instruments.Config import subdomain, headers
import aiohttp

pre_url = f"https://{subdomain}.omnidesk.ru/api/cases/"


async def update_status(case_number, new_status):
    url = f"{pre_url}{case_number}.json"

    body = {"case": {"status": new_status}}

    async with aiohttp.ClientSession() as session:
        await session.put(url, headers=headers, json=body)
