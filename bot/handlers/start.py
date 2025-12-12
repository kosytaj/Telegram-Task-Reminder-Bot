from aiogram import Router, types
from aiogram.filters import CommandStart
from db.models import User
from db.database import get_session

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
async for session in get_session():
user = await session.get(User, message.from_user.id)
if not user:
user = User(tg_id=message.from_user.id, username=message.from_user.username)
session.add(user)
await session.commit()
await message.answer("✅ Вы зарегистрированы! Используйте /create_task чтобы создать задачу.")