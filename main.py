from aiogram import Bot, Dispatcher
import asyncio
from config import BOT_TOKEN
from db.database import init_db
from bot.scheduler import scheduler
from bot.handlers import start, create_task, mytasks, task_actions

async def main():
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(
start.router,
create_task.router,
mytasks.router,
task_actions.router,
)

scheduler.start()
await init_db()
await dp.start_polling(bot)
if name == "main":
asyncio.run(main())