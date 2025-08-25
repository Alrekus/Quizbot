import logging
import random
import os
import json
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Берём токен из переменной окружения
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ Нет API_TOKEN! Установи переменную окружения.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ФАЙЛ ДЛЯ ХРАНЕНИЯ ЛИДЕРБОРДА ---
LEADERBOARD_FILE = "leaderboard.json"

# Загружаем лидерборд при старте
if os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
        leaderboard = json.load(f)
else:
    leaderboard = {}  # {"Имя": [{"score": int, "date": str}, ...]}

# --- ВОПРОСЫ (сюда можно дописать до 50) ---
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "ТОКЕН_ТВОЕГО_БОТА"  # вставь сюда токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ВОПРОСЫ (50 шт.) ---
questions = [
    {"q": "Сколько будет 7 * 8?", "options": ["54", "56", "64", "58"], "a": "56"},
    {"q": "Столица Франции?", "options": ["Берлин", "Мадрид", "Париж", "Рим"], "a": "Париж"},
    {"q": "Корень из 81?", "options": ["8", "9", "7", "11"], "a": "9"},
    {"q": "Кто написал «Евгений Онегин»?", "options": ["Лермонтов", "Пушкин", "Толстой", "Достоевский"], "a": "Пушкин"},
    {"q": "Сколько континентов на Земле?", "options": ["5", "6", "7", "4"], "a": "6"},
    {"q": "Какая планета ближе всего к Солнцу?", "options": ["Земля", "Венера", "Меркурий", "Марс"], "a": "Меркурий"},
    {"q": "Сколько градусов в прямом угле?", "options": ["90", "180", "45", "60"], "a": "90"},
    {"q": "Кто открыл Америку?", "options": ["Магеллан", "Колумб", "Кук", "Васко да Гама"], "a": "Колумб"},
    {"q": "Самая длинная река в мире?", "options": ["Нил", "Амазонка", "Янцзы", "Волга"], "a": "Амазонка"},
    {"q": "Автор романа «Война и мир»?", "options": ["Толстой", "Пушкин", "Гоголь", "Достоевский"], "a": "Толстой"},
    {"q": "Столица Италии?", "options": ["Милан", "Рим", "Флоренция", "Венеция"], "a": "Рим"},
    {"q": "Химический символ воды?", "options": ["O2", "H2O", "CO2", "HO"], "a": "H2O"},
    {"q": "Кто написал «Мёртвые души»?", "options": ["Гоголь", "Толстой", "Тургенев", "Чехов"], "a": "Гоголь"},
    {"q": "Сколько хромосом у человека?", "options": ["42", "44", "46", "48"], "a": "46"},
    {"q": "Сколько планет в Солнечной системе?", "options": ["7", "8", "9", "10"], "a": "8"},
    {"q": "Какая кровь универсальна для переливания?", "options": ["I", "II", "III", "IV"], "a": "I"},
    {"q": "Кто изобрёл лампочку?", "options": ["Эдисон", "Тесла", "Попов", "Фарадей"], "a": "Эдисон"},
    {"q": "Сколько будет 12 * 12?", "options": ["124", "144", "132", "156"], "a": "144"},
    {"q": "Столица Германии?", "options": ["Берлин", "Гамбург", "Мюнхен", "Дрезден"], "a": "Берлин"},
    {"q": "Кто написал пьесу «Гроза»?", "options": ["Островский", "Чехов", "Горький", "Тургенев"], "a": "Островский"},
    {"q": "Самая большая планета в Солнечной системе?", "options": ["Сатурн", "Юпитер", "Уран", "Земля"], "a": "Юпитер"},
    {"q": "Какой газ мы вдыхаем при дыхании?", "options": ["Азот", "Кислород", "Углекислый газ", "Гелий"], "a": "Кислород"},
    {"q": "Сколько месяцев в году имеет 31 день?", "options": ["6", "7", "8", "5"], "a": "7"},
    {"q": "Кто написал «Капитанскую дочку»?", "options": ["Пушкин", "Толстой", "Лермонтов", "Чехов"], "a": "Пушкин"},
    {"q": "Какая самая высокая гора на Земле?", "options": ["Эверест", "Килиманджаро", "Эльбрус", "Монблан"], "a": "Эверест"},
    {"q": "Какой океан самый большой?", "options": ["Атлантический", "Тихий", "Индийский", "Северный Ледовитый"], "a": "Тихий"},
    {"q": "Кто написал «Ревизор»?", "options": ["Гоголь", "Толстой", "Тургенев", "Чехов"], "a": "Гоголь"},
    {"q": "Сколько костей у взрослого человека?", "options": ["206", "210", "196", "201"], "a": "206"},
    {"q": "Формула площади круга?", "options": ["πr²", "2πr", "a²", "ab"], "a": "πr²"},
    {"q": "Кто написал «Детство»?", "options": ["Толстой", "Горький", "Тургенев", "Чехов"], "a": "Толстой"},
    {"q": "Какая страна самая большая по территории?", "options": ["Россия", "Канада", "Китай", "США"], "a": "Россия"},
    {"q": "Сколько будет 15 * 5?", "options": ["60", "65", "70", "75"], "a": "75"},
    {"q": "Столица Японии?", "options": ["Токио", "Осака", "Киото", "Нара"], "a": "Токио"},
    {"q": "Кто написал «Герой нашего времени»?", "options": ["Лермонтов", "Толстой", "Пушкин", "Чехов"], "a": "Лермонтов"},
    {"q": "Какая птица самая большая?", "options": ["Орёл", "Страус", "Пеликан", "Кондор"], "a": "Страус"},
    {"q": "Сколько будет 100 / 4?", "options": ["20", "25", "30", "40"], "a": "25"},
    {"q": "Столица Великобритании?", "options": ["Париж", "Лондон", "Берлин", "Мадрид"], "a": "Лондон"},
    {"q": "Кто написал «Чайку»?", "options": ["Чехов", "Горький", "Толстой", "Пушкин"], "a": "Чехов"},
    {"q": "Сколько океанов на Земле?", "options": ["3", "4", "5", "6"], "a": "5"},
    {"q": "Какая планета известна как красная?", "options": ["Марс", "Венера", "Сатурн", "Юпитер"], "a": "Марс"},
    {"q": "Кто написал «Отцы и дети»?", "options": ["Тургенев", "Толстой", "Пушкин", "Чехов"], "a": "Тургенев"},
    {"q": "Столица Китая?", "options": ["Пекин", "Шанхай", "Гонконг", "Токио"], "a": "Пекин"},
    {"q": "Кто открыл закон всемирного тяготения?", "options": ["Ньютон", "Эйнштейн", "Галилей", "Коперник"], "a": "Ньютон"},
    {"q": "Сколько будет 9²?", "options": ["81", "72", "91", "99"], "a": "81"},
    {"q": "Столица Испании?", "options": ["Барселона", "Мадрид", "Севилья", "Валенсия"], "a": "Мадрид"},
    {"q": "Кто написал «Маленький принц»?", "options": ["Экзюпери", "Толстой", "Гоголь", "Достоевский"], "a": "Экзюпери"},
    {"q": "Самое большое животное на Земле?", "options": ["Слон", "Синий кит", "Жираф", "Кашалот"], "a": "Синий кит"},
    {"q": "Сколько будет 64 : 8?", "options": ["6", "7", "8", "9"], "a": "8"},
    {"q": "Столица Канады?", "options": ["Оттава", "Торонто", "Монреаль", "Ванкувер"], "a": "Оттава"},
    {"q": "Кто написал «Преступление и наказание»?", "options": ["Достоевский", "Толстой", "Чехов", "Гоголь"], "a": "Достоевский"}
]

# --- ДАННЫЕ ИГРОКОВ ---
user_data = {}     # для текущей игры
leaderboard = {}   # для сохранения рекордов

def make_keyboard(options):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in options:
        kb.add(KeyboardButton(opt))
    return kb

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    await message.answer(
        "Привет! 🎓 Это школьная викторина.\n"
        "Команды:\n"
        "👉 /quiz – начать игру\n"
        "👉 /leaderboard – таблица лидеров"
    )

@dp.message_handler(commands=['quiz'])
async def send_question(message: types.Message):
    user_id = message.from_user.id
    shuffled = random.sample(questions, len(questions))  # случайный порядок
    user_data[user_id] = {"score": 0, "index": 0, "quiz": shuffled}
    await ask_question(message)

async def ask_question(message):
    user_id = message.from_user.id
    idx = user_data[user_id]["index"]

    if idx >= len(user_data[user_id]["quiz"]):  # конец
        score = user_data[user_id]["score"]
        username = message.from_user.first_name

        # сохраняем в лидерборд
        if username not in leaderboard or score > leaderboard[username]:
            leaderboard[username] = score

        await message.answer(
            f"🏁 Викторина окончена!\nТвой результат: {score}/{len(user_data[user_id]['quiz'])}",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    q = user_data[user_id]["quiz"][idx]
    kb = make_keyboard(q["options"])
    await message.answer(f"Вопрос {idx+1} из {len(user_data[user_id]['quiz'])}:\n{q['q']}", reply_markup=kb)

@dp.message_handler(commands=['leaderboard'])
async def show_leaderboard(message: types.Message):
    if not leaderboard:
        await message.answer("📊 Лидерборд пока пуст.")
        return

    sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    text = "🏆 Лидерборд:\n"
    for i, (user, score) in enumerate(sorted_lb[:10], start=1):
        text += f"{i}. {user} — {score} очков\n"
    await message.answer(text)

@dp.message_handler()
async def check_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Напиши /quiz чтобы начать игру.")
        return

    idx = user_data[user_id]["index"]
    if idx >= len(user_data[user_id]["quiz"]):
        await message.answer("Игра уже окончена. Напиши /quiz чтобы начать заново.")
        return

    current_q = user_data[user_id]["quiz"][idx]
    correct = current_q["a"].lower()
    answer = message.text.strip().lower()

    if answer == correct:
        user_data[user_id]["score"] += 1
        await message.answer("✅ Правильно!")
    else:
        await message.answer(f"❌ Неправильно. Правильный ответ: {current_q['a']}")

    # следующий вопрос
    user_data[user_id]["index"] += 1
    await ask_question(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# --- ДАННЫЕ ИГРОКОВ ---
user_data = {}

def save_leaderboard():
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)

def make_keyboard(options):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in options:
        kb.add(KeyboardButton(opt))
    return kb

def get_leaderboard_with_rank(username=None):
    if not leaderboard:
        return "📊 Лидерборд пока пуст."

    best_scores = {user: max(attempt["score"] for attempt in scores) for user, scores in leaderboard.items()}
    sorted_lb = sorted(best_scores.items(), key=lambda x: x[1], reverse=True)

    text = "🏆 Топ-3 игроков:\n"
    for i, (user, score) in enumerate(sorted_lb[:3], start=1):
        text += f"{i}. {user} — {score} очков\n"

    if username and username in best_scores:
        rank = [u for u, _ in sorted_lb].index(username) + 1
        best_score = best_scores[username]
        if rank > 3:
            text += f"\n📌 {username}, твоё место: {rank}/{len(sorted_lb)} (лучший результат: {best_score})"
    return text

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    await message.answer(
        "Привет! 🎓 Это школьная викторина.\n"
        "Команды:\n"
        "👉 /quiz – начать игру\n"
        "👉 /leaderboard – таблица лидеров\n"
        "👉 /myresults – моя история попыток"
    )

@dp.message_handler(commands=['quiz'])
async def send_question(message: types.Message):
    user_id = message.from_user.id
    shuffled = random.sample(questions, len(questions))
    user_data[user_id] = {"score": 0, "index": 0, "quiz": shuffled}
    await ask_question(message)

async def ask_question(message):
    user_id = message.from_user.id
    idx = user_data[user_id]["index"]

    if idx >= len(user_data[user_id]["quiz"]):
        score = user_data[user_id]["score"]
        username = message.from_user.first_name

        if username not in leaderboard:
            leaderboard[username] = []
        leaderboard[username].append({
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_leaderboard()

        await message.answer(
            f"🏁 Викторина окончена!\n"
            f"Твой результат: {score}/{len(user_data[user_id]['quiz'])}\n\n"
            f"{get_leaderboard_with_rank(username)}",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    q = user_data[user_id]["quiz"][idx]
    kb = make_keyboard(q["options"])
    await message.answer(f"Вопрос {idx+1} из {len(user_data[user_id]['quiz'])}:\n{q['q']}", reply_markup=kb)

@dp.message_handler(commands=['leaderboard'])
async def show_leaderboard(message: types.Message):
    username = message.from_user.first_name
    await message.answer(get_leaderboard_with_rank(username))

@dp.message_handler(commands=['myresults'])
async def show_my_results(message: types.Message):
    username = message.from_user.first_name
    if username not in leaderboard:
        await message.answer("❌ У тебя ещё нет результатов. Напиши /quiz чтобы сыграть!")
        return

    attempts = leaderboard[username]
    text = f"📜 История твоих попыток ({len(attempts)}):\n"
    for i, attempt in enumerate(attempts, start=1):
        text += f"{i}. {attempt['date']} — {attempt['score']} очков\n"
    text += f"\n🏆 Твой лучший результат: {max(a['score'] for a in attempts)}"
    await message.answer(text)

@dp.message_handler()
async def check_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Напиши /quiz чтобы начать игру.")
        return

    idx = user_data[user_id]["index"]
    if idx >= len(user_data[user_id]["quiz"]):
        await message.answer("Игра уже окончена. Напиши /quiz чтобы начать заново.")
        return

    current_q = user_data[user_id]["quiz"][idx]
    correct = current_q["a"].lower()
    answer = message.text.strip().lower()

    if answer == correct:
        user_data[user_id]["score"] += 1
        await message.answer("✅ Правильно!")
    else:
        await message.answer(f"❌ Неправильно. Правильный ответ: {current_q['a']}")

    user_data[user_id]["index"] += 1
    await ask_question(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
