from aiogram import Dispatcher, Bot

from bot.handlers import register_message_handlers, register_admin_handlers

dp = Dispatcher()


def register_handlers():
    register_message_handlers(dp)
    register_admin_handlers(dp)


async def start_bot(token):
    bot = Bot(token)
    register_handlers()
    await dp.start_polling(bot)