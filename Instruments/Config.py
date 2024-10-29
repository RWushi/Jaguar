import os
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from aiohttp import web
from fastapi import FastAPI
import base64

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

app = web.Application()

fapi = FastAPI()

admins = (os.getenv('ADMIN1'), os.getenv('ADMIN2'), os.getenv('ADMIN3'))

email = os.getenv('EMAIL')
api_key = os.getenv('API_KEY')
subdomain = os.getenv('SUBDOMAIN')

auth_string = f"{email}:{api_key}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

headers = {"Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/json"}

channel = os.getenv('CHANNEL')

DATABASE_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'port': os.getenv("DB_PORT")}


class DB:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(**DATABASE_CONFIG)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


class States(StatesGroup):
    date = State()

    full_name = State()
    phone = State()
    cities = State()
    confirmation = State()
    choose_category = State()

    medical = State()
    driving = State()
    theory = State()
    internal_exam = State()
    gibdd_exam = State()
    payment = State()

    categories_operator = State()
    category_operator = State()
    rate_operator = State()
    operator = State()

    rate = State()


categories_ru_en = {
    "Медицинская справка": "medical",
    "Вождение": "driving",
    "Теория": "theory",
    "Внутренние экзамены": "internal_exam",
    "Экзамен в ГИБДД": "gibdd_exam",
    "Оплата услуг": "payment",
    "Оператор": "operator"
}

categories_en_ru = {
    "medical": "Медицинская справка",
    "driving": "Вождение",
    "theory": "Теория",
    "internal_exam": "Внутренние экзамены",
    "gibdd_exam": "Экзамен в ГИБДД",
    "payment": "Оплата услуг",
    "operator": "Оператор"
}

city_groups = {'Воронеж': 66761, 'Москва': 72756, 'Санкт-Петербург': 78223}

user_questions = {5419806659: ['Воронеж'], 5863595924: ['Санкт-Петербург']}  # {user_id: ['Москва', 'Медицинская справка', 1]}

user_operator_state = {}
operators_messages = {}
reasons_list = []
reminder_cases = []
