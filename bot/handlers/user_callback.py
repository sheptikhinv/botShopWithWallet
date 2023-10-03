from aiogram import Router, F, types, Dispatcher

from bot.keyboards import user_buttons
from bot.misc import format_product
from database import Product

router = Router(name="user_callback")


@router.callback_query(F.data.contains("get"))
async def get_product_by_user(callback_query: types.CallbackQuery):
    link = callback_query.data.split()[2]
    product = Product.get_by_link(link)
    text = await format_product(product)
    reply_markup = user_buttons(product)
    if product.file_id is not None:
        await callback_query.message.answer_photo(caption=text, photo=product.file_id, reply_markup=reply_markup)
    else:
        await callback_query.message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(F.data.contains("buy"))
async def create_order(callback_query: types.CallbackQuery):
    link = callback_query.data.split()[2]
    product = Product.get_by_link(link)
    await callback_query.message.answer(f"You gonna buy:\n"
                                        f"Product: {product.title}\n"
                                        f"Price: {product.price} {product.currency_code}\n\n"
                                        f"Вот тут должна быть кнопка на оплату через WalletAPI")


def register_callback_handlers(dp: Dispatcher):
    dp.include_router(router)
