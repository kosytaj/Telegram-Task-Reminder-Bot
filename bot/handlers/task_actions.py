from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states import TaskReschedule
from db.models import Task, TaskStatus
from db.database import get_session
from bot.scheduler import schedule_task
from datetime import datetime

router = Router()

@router.callback_query(F.data.startswith("done:"))
async def mark_done(callback: types.CallbackQuery):
task_id = int(callback.data.split(":"))
async for session in get_session():
task = await session.get(Task, task_id)
if task and task.assignee_id == callback.from_user.id:
task.status = TaskStatus.DONE
await session.commit()
await callback.message.answer("✅ Отмечено как выполнено.")
await callback.bot.send_message(task.creator_id, f"📌 Задача '{task.title}' выполнена.")

@router.callback_query(F.data.startswith("cancel:"))
async def cancel_task(callback: types.CallbackQuery):
task_id = int(callback.data.split(":"))
async for session in get_session():
task = await session.get(Task, task_id)
if task and task.assignee_id == callback.from_user.id:
task.status = TaskStatus.CANCELLED
await session.commit()
await callback.message.answer("🚫 Задача отменена.")
await callback.bot.send_message(task.creator_id, f"📌 Задача '{task.title}' отменена.")

@router.callback_query(F.data.startswith("reschedule:"))
async def start_reschedule(callback: types.CallbackQuery, state: FSMContext):
await state.set_state(TaskReschedule.waiting_new_datetime)
await state.update_data(task_id=int(callback.data.split(":")))
await callback.message.answer("Введите новую дату/время (ГГГГ-ММ-ДД ЧЧ:ММ):")

@router.message(TaskReschedule.waiting_new_datetime)
async def do_reschedule(message: types.Message, state: FSMContext, bot: Bot):
try:
dt = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")
except ValueError:
await message.answer("⚠️ Неверный формат.")
return

data = await state.get_data()
task_id = data.get("task_id")

async for session in get_session():
task = await session.get(Task, task_id)
task.scheduled_at = dt
task.status = TaskStatus.RESCHEDULED
await session.commit()

schedule_task(bot, task.id, dt)
await message.answer("🔁 Задача перенесена.")
await bot.send_message(task.creator_id, f"📌 Задача '{task.title}' была перенесена.")

await state.clear()
