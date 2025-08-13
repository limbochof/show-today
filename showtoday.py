from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.filters import Command
import asyncio

# 🔐 Токен бота
import os
TOKEN = os.getenv("TOKEN")

# 👥 Пользователи, которых можно упоминать и которые могут "открывать"
GATE_RESPONDERS = ["MadiyarYntykbay", "Tinbrawl", ]
OPEN_RESPONDERS = ["teemudzhinn", "Garmaevvlad", "danayergali"]

bot = Bot(token=TOKEN)
dp = Dispatcher()


# 📥 Команда запроса на открытие ворот (Айтиева)
@dp.message(Command("gate"))
async def request_gate(message: Message):
    requester = message.from_user.username or message.from_user.full_name
    gate_location = "с Айтиева"
    tagged_users = " ".join([f"@{u}" for u in GATE_RESPONDERS])

    await message.delete()
    
    text = (
        f"🔐 Запрос на открытие ворот {gate_location} от @{requester}.\n\n"
        f"{tagged_users}\n\n"
        
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Не Открыто", callback_data="gate_opened")]
    ])

    await message.answer(text, reply_markup=keyboard)


# 📥 Команда запроса на открытие шлагбаума
@dp.message(Command("open"))
async def request_barrier(message: Message):
    requester = message.from_user.username or message.from_user.full_name
    tagged_users = " ".join([f"@{u}" for u in OPEN_RESPONDERS])

    await message.delete()
    
    text = (
        f"🛡 Запрос на открытие шлагбаума от @{requester}.\n\n"
        f"{tagged_users}\n\n"
        
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Не Открыто", callback_data="barrier_opened")]
    ])

    await message.answer(text, reply_markup=keyboard)


# 🟢 Обработка кнопки "Открыто" — для ворот
@dp.callback_query(lambda c: c.data == "gate_opened")
async def handle_gate_opened(callback: types.CallbackQuery):
    opener = callback.from_user.username or callback.from_user.full_name
    if opener not in GATE_RESPONDERS:
        await callback.answer("⛔ У вас нет прав открывать ворота", show_alert=True)
        return

    # Изменение текста на кнопке, сообщение не трогаем
    new_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ Открыл @{opener}", callback_data="noop")]
    ])
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.answer("Готово!")


# 🟢 Обработка кнопки "Открыто" — для шлагбаума
@dp.callback_query(lambda c: c.data == "barrier_opened")
async def handle_barrier_opened(callback: types.CallbackQuery):
    opener = callback.from_user.username or callback.from_user.full_name
    if opener not in OPEN_RESPONDERS:
        await callback.answer("⛔ У вас нет прав открывать шлагбаум", show_alert=True)
        return

    new_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"✅ Открыл @{opener}", callback_data="noop")]
    ])
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.answer("Готово!")


# 🔒 Заглушка на дальнейшее нажатие (чтобы кнопка ничего не делала)
@dp.callback_query(lambda c: c.data == "noop")
async def noop(callback: types.CallbackQuery):
    await callback.answer("Уже открыто ✅", show_alert=True)


# 📋 Установка команд с подсказками
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="open", description="🛡 Запрос на открытие шлагбаума"),
        BotCommand(command="gate", description="🚪 Запрос на открытие ворот с Айтиева"),
    ]
    await bot.set_my_commands(commands)


# ▶️ Запуск бота
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
