from aiogram import Router, F, types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards import user_buttons, contact_button, empty_button, pay_button
from bot.misc import format_product, create_new_order, checking_and_finishing_order
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
    await callback_query.answer()


@router.callback_query(F.data.contains("buy"))
async def create_order(callback_query: types.CallbackQuery):
    link = callback_query.data.split()[2]
    product = Product.get_by_link(link)
    order = await create_new_order(product, callback_query.from_user.id)
    await callback_query.message.answer(text=f"You gonna buy:\n"
                                             f"Product: {product.title}\n"
                                             f"Price: {product.price} {product.currency_code}\n\n",
                                        reply_markup=pay_button(order.pay_link))
    await callback_query.answer()
    if callback_query.message.photo:
        await callback_query.message.edit_caption(caption=callback_query.message.caption, reply_markup=empty_button())
    else:
        await callback_query.message.edit_text(text=callback_query.message.text, reply_markup=empty_button())
    await checking_and_finishing_order(order=order, callback_query=callback_query, product=product)


def register_callback_handlers(dp: Dispatcher):
    dp.include_router(router)
