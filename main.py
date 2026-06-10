from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
from models import ItemsResponse
import os, asyncio, logging, sys, requests


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CLIENT_ID = os.getenv("AVITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("AVITO_CLIENT_SECRET")

def getToken() -> str:

    url = "https://api.avito.ru/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    r = requests.post(url, data=data)

    return r.json()['access_token']


ACCESS_TOKEN = getToken()
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}! Это телеграм бот для управления объявлениями Avito\n\nСписок команд:\n/get - получить все мои объявления\n")

@router.message(Command("get"))
async def get_handler(message: Message) -> None:
    urlGetData = "https://api.avito.ru/core/v1/items"
    res = requests.get(urlGetData, headers=headers)

    data = ItemsResponse.model_validate(res.json())

    answers = [""]
    mes = 0
    c = 0
    for item in data.resources:
        i = f"{c+1}\n{item.title} {item.price}р.\n{item.category.name}\n{item.address}\n{item.status} {item.url}\n\n\n" 
        l = len(answers[mes] + i)
        if (l > 4096):
            answers.append(i)
            mes +=1
        else:
            answers[mes] += i

        c += 1
    for i in answers:
        await message.answer(f"обьявления ербола крутого перца\n{i}")















async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="get",
            description="Получить список объявлений"
        ),
        BotCommand(
            command="start",
            description="Запустить бота и получить салам"
        ),
    ]

    await bot.set_my_commands(commands)

@router.message()
async def debug(message: Message):
    print("Получено:", message.text)

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await set_commands(bot)
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
