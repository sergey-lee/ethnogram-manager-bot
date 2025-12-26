import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_GROUP_ID = -123456789  # ID группы с операторами

bot = Bot(token=TOKEN)
dp = Dispatcher()

users_waiting = {}  # user_id -> last_message_id_for_reply mapping

# --- Keyboards ---
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Что такое этнограм?")],
        [KeyboardButton(text="Что такое подписка Plus?")],
        [KeyboardButton(text="У Вас есть другие вопросы?")]
    ],
    resize_keyboard=True
)

back_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Назад")]],
    resize_keyboard=True
)


# ========= User UI =========

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("Здравствуйте! Чем могу помочь?", reply_markup=main_kb)


@dp.message(F.text == "Что такое этнограм?")
async def about_etnogram(message: types.Message):
    await message.answer("Этнограм — бла бла бла...", reply_markup=back_kb)


@dp.message(F.text == "Что такое подписка Plus?")
async def about_plus(message: types.Message):
    await message.answer("Подписка Plus — бла бла бла...", reply_markup=back_kb)


@dp.message(F.text == "У Вас есть другие вопросы?")
async def ask_question(message: types.Message):
    await message.answer("Напишите ваш вопрос одним сообщением ↓")


@dp.message(F.text == "Назад")
async def back(message: types.Message):
    await message.answer("Главное меню", reply_markup=main_kb)


# ========= Forward questions to admin group =========

@dp.message(F.chat.type == "private")  # любой текст от юзера
async def user_question(message: types.Message):
    forwarded = await bot.send_message(
        ADMIN_GROUP_ID,
        f"❓ Вопрос от {message.from_user.full_name} (@{message.from_user.username})\nID:{message.from_user.id}\n\n{message.text}"
    )

    users_waiting[forwarded.message_id] = message.from_user.id  # связь reply → user
    await message.answer("Спасибо! Ваш вопрос передан оператору 🙌")


# ========= Reply from admin group back to user =========

@dp.message(F.chat.id == ADMIN_GROUP_ID & F.reply_to_message)
async def admin_reply(message: types.Message):
    replied_msg = message.reply_to_message.message_id

    if replied_msg in users_waiting:
        user_id = users_waiting[replied_msg]
        await bot.send_message(user_id, f"Ответ оператора:\n{message.text}")
        await message.answer("📤 Отправлено пользователю")
    else:
        await message.answer("⚠ Не найден пользователь для этого сообщения")


# ========= Run =========

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
