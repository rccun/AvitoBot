from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import os, asyncio, logging, sys, requests
from aiogram.client.session.aiohttp import AiohttpSession


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("AVITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("AVITO_CLIENT_SECRET")

url = "https://api.avito.ru/token"

data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

r = requests.post(url, data=data)
ACCESS_TOKEN = r.json()['access_token']
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
urlGetData = "https://api.avito.ru/core/v1/items"

bot = Bot(token=BOT_TOKEN)
router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}! (ербол огромный лох)")

@router.message()
async def debug(message: Message):
    print("Получено:", message.text)

@router.message("/get")
async def get_handler(message: Message) -> None:
    res = requests.get(urlGetData, headers=headers)
    await message.answer(f"Привет, {message.from_user.full_name}! {res}")

async def main() -> None:
    session = AiohttpSession(proxy="socks5://127.0.0.1:10809") # принудительное подключение к прокси с использованием порта happ
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
