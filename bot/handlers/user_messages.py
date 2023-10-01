from aiogram import Router, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject

from bot.keyboards import list_of_products
from bot.keyboards.inline import make_order
from bot.misc import format_product
from database import User, Product

router = Router(name="user_messages")


@router.message(Command("start"))
async def start_command(message: types.Message, command: CommandObject):
    user = User(message.from_user.id, "user", message.from_user.first_name)
    if user.is_user_new():
        user.add_to_database()
    if command.args is None:
        await message.answer('Вы можете отправить "/products" чтоб увидеть все товары!')
    else:
        product = Product.get_by_link(command.args)
        if product.status != "active":
            await message.answer('Данного товара сейчас нет в наличии, вы можете выбрать что-то другое в "/products"')
            return
        text = await format_product(product)
        reply_markup = reply_markup = make_order(product)
        if product.file_id is not None:
            await message.answer_photo(caption=text, photo=product.file_id, reply_markup=reply_markup)
        else:
            await message.answer(text=text, reply_markup=reply_markup)


@router.message(Command("products"))
async def get_products_by_user(message: types.Message):
    await message.answer(
        text="Вот все товары:",
        reply_markup=list_of_products(is_admin=False)
    )


def register_message_handlers(dp: Dispatcher):
    dp.include_router(router)
