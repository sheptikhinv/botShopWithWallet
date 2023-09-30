from aiogram import Router, Dispatcher, types
from aiogram.filters.command import Command

from database import User

router = Router(name="messages")


@router.message(Command("start"))
async def start_command(message: types.Message):
    user = User(message.from_user.id, "user", message.from_user.first_name)
    if user.is_user_new():
        user.add_to_database()
    await message.answer("Приветственное сообщение")


def register_message_handlers(dp: Dispatcher):
    dp.include_router(router)