from .Config import DB
from datetime import date


async def add_new_user(user_id, username):
    async with DB() as conn:
        await conn.execute('''INSERT INTO users (id, username) 
            VALUES ($1, $2) ON CONFLICT (id) DO NOTHING''', user_id, username)


async def check_status(user_id):
    async with DB() as conn:
        return await conn.fetchval('SELECT confirmed FROM users WHERE id = $1', user_id)


async def set_full_name(user_id, full_name):
    async with DB() as conn:
        await conn.execute('UPDATE users SET full_name = $2 WHERE id = $1', user_id, full_name)


async def set_phone(user_id, phone):
    async with DB() as conn:
        await conn.execute('UPDATE users SET phone = $2 WHERE id = $1', user_id, phone)


async def set_city(user_id, city):
    async with DB() as conn:
        await conn.execute('UPDATE users SET city = $2 WHERE id = $1', user_id, city)


async def get_full_name(user_id):
    async with DB() as conn:
        return await conn.fetchval('SELECT full_name FROM users WHERE id = $1', user_id)


async def get_phone(user_id):
    async with DB() as conn:
        return await conn.fetchval('SELECT phone FROM users WHERE id = $1', user_id)


async def confirm_status(user_id):
    async with DB() as conn:
        await conn.execute('UPDATE users SET confirmed = True WHERE id = $1', user_id)


async def get_user_data(user_id):
    async with DB() as conn:
        row = await conn.fetchrow('SELECT full_name, username, phone FROM users WHERE id = $1', user_id)
        return row['phone'], row['username'], row['full_name']


async def get_appeal_number(user_id):
    async with DB() as conn:
        return await conn.fetchval('SELECT appeal_number FROM users WHERE id = $1', user_id)


async def set_appeal_number(user_id, case_number):
    async with DB() as conn:
        await conn.execute('UPDATE users SET appeal_number = $2 WHERE id = $1', user_id, case_number)


async def operator_click(city, category, number):
    async with DB() as conn:
        await conn.execute('''
            INSERT INTO statistics (question_id, city, category, number, date, operator_calls)
            VALUES
                ((SELECT id FROM questions WHERE city = $1 AND category = $2 AND number = $3),
                $1, $2, $3, $4, 1)
            ON CONFLICT (city, category, number, date) DO UPDATE
            SET operator_calls = statistics.operator_calls + 1
        ''', city, category, number, date.today())


async def question_click(city, category, number):
    async with DB() as conn:
        await conn.execute('''
            INSERT INTO statistics (question_id, city, category, number, date, clicks)
            VALUES
                ((SELECT id FROM questions WHERE city = $1 AND category = $2 AND number = $3),
                $1, $2, $3, $4, 1)
            ON CONFLICT (city, category, number, date) DO UPDATE
            SET clicks = statistics.clicks + 1
        ''', city, category, number, date.today())
