from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def task_action_keyboard(task_id: int):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(text="✅ Выполнено", callback_data=f"done:{task_id}")],
[InlineKeyboardButton(text="🔁 Перенести", callback_data=f"reschedule:{task_id}")],
[InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel:{task_id}")],
])