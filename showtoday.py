import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.filters import Command
from zadarma_api import ZadarmaAPI

# 🔐 Токен Telegram-бота
TOKEN = os.getenv("TOKEN")

# 🔐 Данные Zadarma
ZD_API_KEY = os.getenv("c41558294371a471c163")
ZD_API_SECRET = os.getenv("02974ac60eaee64523c1")

# 📞 Номера
BARRIER_NUMBER = "+77001111111"  # номер для шлагбаума
GATE_NUMBER = "+77762268953"     # номер для ворот
CALL_FROM = "+77009999999"       # твой номер/SIP от Zadarma

bot = Bot(token=TOKEN)
dp = Dispatcher()
zd_api = ZadarmaAPI(ZD_API_KEY, ZD_API_SECRET)


# 📞 Функция звонка через Zadarma
async def zadarma_call(to_number: str):
    try:
        response = zd_api.call("/request/callback/", {
            "from": CALL_FROM,
            "to": to_number
        })
        print(f"📞 Звонок на {to_number}: {response}")
    except Exception as e:
        print(f"❌ Ошибка звонка на {to_number}: {e}")


# 🚪 Команда для ворот
@dp.message(Command("gate"))
async def request_gate(message: types.Message):
    requester = message.from_user.username or message.from_user.full_name
    await message.delete()

    # Звонок на номер ворот
    await zadarma_call(GATE_NUMBER)

    await message.answer(f"🚪 Ворота открыты. Открыл @{requester}")


# 🛡 Команда для шлагбаума
@dp.message(Command("open"))
async def request_barrier(message: types.Message):
    requester = message.from_user.username or message.from_user.full_name
    await message.delete()

    # Звонок на номер шлагбаума
    await zadarma_call(BARRIER_NUMBER)

    await message.answer(f"🛡 Шлагбаум открыт. Открыл @{requester}")


# 📋 Установка команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="open", description="🛡 Открыть шлагбаум"),
        BotCommand(command="gate", description="🚪 Открыть ворота"),
    ]
    await bot.set_my_commands(commands)


# ▶️ Запуск
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
