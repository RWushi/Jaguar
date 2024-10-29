import psycopg2
from .Config import DATABASE_CONFIG
import asyncio

phrases = {}
#reasons = []


async def load_phrases():
    #global reasons
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT city, category, number, question, answer FROM questions")
    rows = cursor.fetchall()
    for row in rows:
        city, category, number, question, answer = row
        phrases.setdefault(city, {}).setdefault(category, {})[number] = \
            {'question': question, 'answer': answer }

    #cursor.execute("SELECT reason FROM reasons")
    #rows = cursor.fetchall()
    #reasons = [row[0] for row in rows]

    cursor.close()
    conn.close()


async def get_answer(city, category, number):
    city_data = phrases.get(city)
    if not city_data:
        return "Ошибка: администратор не добавил этот город в базу данных"

    category_data = city_data.get(category)
    if not category_data:
        return "Ошибка: администратор не добавил эту категорию в базу данных"

    answer_data = category_data.get(number)
    if not answer_data:
        return "Ошибка: администратор не добавил этот номер вопроса в базу данных"

    answer = answer_data.get('answer', "Ошибка: администратор не добавил этого ответа в базу данных")
    return answer


async def get_question(city, category, number):
    city_data = phrases.get(city)
    if not city_data:
        return "Ошибка: администратор не добавил этот город в базу данных"

    category_data = city_data.get(category)
    if not category_data:
        return "Ошибка: администратор не добавил эту категорию в базу данных"

    question_data = category_data.get(number)
    if not question_data:
        return "Ошибка: администратор не добавил этот номер вопроса в базу данных"

    question = question_data.get('question', "Ошибка: администратор не добавил этого вопроса в базу данных")
    return question


async def get_questions(city, category):
    city_data = phrases.get(city)
    if not city_data:
        return "Ошибка: администратор не добавил этот город в базу данных", 0

    category_data = city_data.get(category)
    if not category_data:
        return "Ошибка: администратор не добавил эту категорию в базу данных", 0

    sorted_category_data = dict(sorted(category_data.items()))

    questions = [item.get('question', "Ошибка: вопрос не найден") for item in sorted_category_data.values()]
    if not questions:
        return "Ошибка: в категории нет вопросов", 0

    formatted_questions = "\n".join([f"{i + 1}) {question}" for i, question in enumerate(questions)])

    return formatted_questions, len(questions)


asyncio.run(load_phrases())
