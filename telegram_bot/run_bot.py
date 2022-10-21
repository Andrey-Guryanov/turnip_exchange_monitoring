import os
import asyncio
from time import sleep
from dotenv import load_dotenv
from aiogram import Router, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from globals import bot
from components import (
    router_task_no_cost,
    router_task_cost,
    router_control_users, )
from components.create_message_task import create_messages

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
    # scheduler.start()
    # scheduler.add_job(create_messages, 'interval', seconds=10)
    # loop = asyncio.get_event_loop()
    # loop.create_task(create_messages())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
