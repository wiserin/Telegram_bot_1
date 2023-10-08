import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher
from app.handlers.user import user_router
from app.handlers.admin import admin_router
from app.database.models import start_db
from bot import bot


# Launching a bot, getting a token
async def main():
    start_db
    load_dotenv()
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())