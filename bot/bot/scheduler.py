from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.models import Task, TaskStatus
from db.database import async_session
from bot.keyboards import task_action_keyboard
from aiogram import Bot

scheduler = AsyncIOScheduler()

def schedule_task(bot: Bot, task_id: int, when):
scheduler.add_job(notify_executor, "date", run_date=when, args=[bot, task_id], id=f"task_{task_id}", replace_existing=True)

async def notify_executor(bot: Bot, task_id: int):
async with async_session() as session:
task = await session.get(Task, task_id)
if task and task.status == TaskStatus.PENDING:
await bot.send_message(
chat_id=task.assignee_id,
text=f"🔔 Напоминание:\n📌 {task.title}\n🕒 {task.scheduled_at.strftime('%Y-%m-%d %H:%M')}",
reply_markup=task_action_keyboard(task.id)
)