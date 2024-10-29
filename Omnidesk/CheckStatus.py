from Instruments.Config import subdomain, headers
import aiohttp

pre_url = f"https://{subdomain}.omnidesk.ru/api/cases/"


async def check_status(case_number):
    url = f"{pre_url}{case_number}.json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data['case']['status'], data['case']['user_id']
