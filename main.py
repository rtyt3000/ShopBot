import asyncio
import logging

from config import bot, dp
from db.database import create_tables
from handlers import commands, profile, orders, admin

logging.basicConfig(level=logging.WARN)


async def main():
    dp.include_routers(commands.router, profile.router, orders.router, admin.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    create_tables()
    asyncio.run(main())
