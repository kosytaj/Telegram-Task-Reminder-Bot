from aiogram import Router, types
from db.database import get_session
from db.models import Task, TaskStatus
from bot.keyboards import task_action_keyboard

router = Router()

@router.message(lambda msg: msg.text == "/mytasks")
async def mytasks(message: types.Message):
async for session in get_session():
result = await session.execute(
Task.table.select().where(
(Task.assignee_id == message.from_user.id) &
(Task.status == TaskStatus.PENDING)
)
)
tasks = result.fetchall()
if not tasks:
await message.answer("📭 У вас нет активных задач.")
return

for row in tasks:
t = row._mapping
await message.answer(f"📌 {t['title']} — {t['scheduled_at'].strftime('%Y-%m-%d %H:%M')}",
reply_markup=task_action_keyboard(t['id']))