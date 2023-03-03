import asyncio
import os

from dotenv import load_dotenv

from bot.Bot import Bot

load_dotenv()

username = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')


async def main():
    bot = Bot()
    await bot.init(username, password)
    input("press close to exit")


if __name__ == "__main__":
    asyncio.run(main())
