import os
import asyncio
from dotenv import load_dotenv
from aiogram import Router, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from globals import bot
from components import (
    router_task_no_cost,
    router_task_cost,
    router_control_users, )
from components.sender import send_messages_task

try:
    from common_modules.app_settings import load_settings
    from common_modules.model_mongo import Mongo_db
except ModuleNotFoundError:
    import sys
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    from common_modules.app_settings import load_settings
    from common_modules.model_mongo import Mongo_db

load_dotenv()

dp = Dispatcher()
router = Router()
scheduler = AsyncIOScheduler()


async def main() -> None:
    dp.include_router(router_control_users.router)
    dp.include_router(router_task_no_cost.router)
    dp.include_router(router_task_cost.router)
    scheduler.start()
    scheduler.add_job(send_messages_task, 'interval', seconds=10, args=(bot,))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
