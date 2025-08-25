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
questions = [
    {"q": "Сколько будет 7 * 8?", "options": ["54", "56", "64", "58"], "a": "56"},
    {"q": "Столица Франции?", "options": ["Берлин", "Мадрид", "Париж", "Рим"], "a": "Париж"},
    {"q": "Корень из 81?", "options": ["8", "9", "7", "11"], "a": "9"},
    {"q": "Кто написал «Евгений Онегин»?", "options": ["Лермонтов", "Пушкин", "Толстой", "Достоевский"], "a": "Пушкин"},
    {"q": "Сколько континентов на Земле?", "options": ["5", "6", "7", "4"], "a": "6"},
    # ... добавь остальные вопросы
]

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
