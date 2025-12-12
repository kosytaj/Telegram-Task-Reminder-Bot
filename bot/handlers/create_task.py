from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states import TaskCreation
from db.models import Task, User
from db.database import get_session
from datetime import datetime
from bot.scheduler import schedule_task

router = Router()

@router.message(F.text == "/create_task")
async def start_create(message: types.Message, state: FSMContext):
await message.answer("Введите @username получателя задачи или 'me' — себе:")
await state.set_state(TaskCreation.choosing_assignee)

@router.message(TaskCreation.choosing_assignee)
async def input_assignee(message: types.Message, state: FSMContext):
assignee = message.text.strip().lstrip("@")
assignee_id = None

async for session in get_session():
if assignee.lower() == "me":
assignee_id = message.from_user.id
else:
result = await session.execute(User.__table__.select().where(User.username == assignee))
user = result.first()
if user:
assignee_id = user._mapping["tg_id"]

if not assignee_id:
await message.reply("Пользователь не найден.")
return

await state.update_data(assignee_id=assignee_id)
await message.answer("Введите заголовок задачи:")
await state.set_state(TaskCreation.entering_title)
@router.message(TaskCreation.entering_title)
async def input_title(message: types.Message, state: FSMContext):
await state.update_data(title=message.text.strip())
await message.answer("Введите дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ (например 2024-07-01 14:30):")
await state.set_state(TaskCreation.setting_datetime)

@router.message(TaskCreation.setting_datetime)
async def input_datetime(message: types.Message, state: FSMContext, bot: Bot):
try:
dt = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")
except ValueError:
await message.answer("⚠️ Неверный формат даты. Попробуйте снова.")
return

data = await state.get_data()
async for session in get_session():
task = Task(
title=data["title"],
creator_id=message.from_user.id,
assignee_id=data["assignee_id"],
scheduled_at=dt
)
session.add(task)
await session.commit()

schedule_task(bot, task.id, dt)
await message.answer("✅ Задача создана и запланирована.")
await state.clear()