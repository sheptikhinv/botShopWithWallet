from aiogram import Router, types, F, Dispatcher
from aiogram.fsm.context import FSMContext

from bot.filters import IsAdmin
from bot.keyboards import admin_buttons
from bot.misc import format_product_for_admin
from bot.states import EditingProduct
from database import Product

router = Router(name="admin_callback")


@router.callback_query(F.data.contains("get"), IsAdmin())
async def get_product_for_admin(callback_query: types.CallbackQuery):
    link = callback_query.data.split()[2]
    product = Product.get_by_link(link)
    text = await format_product_for_admin((await callback_query.bot.get_me()).username, product)
    reply_markup = admin_buttons(product)
    if product.file_id is not None:
        await callback_query.message.answer_photo(caption=text, photo=product.file_id, reply_markup=reply_markup)
    else:
        await callback_query.message.answer(text=text, reply_markup=reply_markup)


@router.callback_query(F.data.contains("change_status"), IsAdmin())
async def change_status(callback_query: types.CallbackQuery):
    link = callback_query.data.split()[2]
    product = Product.get_by_link(link)
    product.change_status()
    text = await format_product_for_admin((await callback_query.bot.get_me()).username, product)
    await callback_query.message.answer("Status changed!")


@router.callback_query(F.data.contains("change_title"), IsAdmin())
async def change_title(callback_query: types.CallbackQuery, state: FSMContext):
    link = callback_query.data.split()[2]
    await callback_query.message.answer("Enter new title:")
    await state.set_state(EditingProduct.editing_title)
    await state.update_data(product_link=link)


@router.callback_query(F.data.contains("change_description"), IsAdmin())
async def change_description(callback_query: types.CallbackQuery, state: FSMContext):
    link = callback_query.data.split()[2]
    await callback_query.message.answer("Enter new description:")
    await state.set_state(EditingProduct.editing_description)
    await state.update_data(product_link=link)


@router.callback_query(F.data.contains("change_price"), IsAdmin())
async def change_price(callback_query: types.CallbackQuery, state: FSMContext):
    link = callback_query.data.split()[2]
    await callback_query.message.answer("Enter new price (digits only):")
    await state.set_state(EditingProduct.editing_price)
    await state.update_data(product_link=link)


@router.callback_query(F.data.contains("change_currency"), IsAdmin())
async def change_currency_code(callback_query: types.CallbackQuery, state: FSMContext):
    link = callback_query.data.split()[2]
    await callback_query.message.answer("Enter new currency code")
    await state.set_state(EditingProduct.editing_currency_code)
    await state.update_data(product_link=link)


@router.callback_query(F.data.contains("change_amount"), IsAdmin())
async def change_amount(callback_query: types.CallbackQuery, state: FSMContext):
    link = callback_query.data.split()[2]
    await callback_query.message.answer("Enter new amount (digits only):")
    await state.set_state(EditingProduct.editing_amount)
    await state.update_data(product_link=link)


@router.callback_query(F.data.contains("change_file_id"), IsAdmin())
async def change_file_id(callback_query: types.CallbackQuery, state: FSMContext):
    link = callback_query.data.split()[2]
    await callback_query.message.answer("Send new product photo:")
    await state.set_state(EditingProduct.editing_file_id)
    await state.update_data(product_link=link)


@router.callback_query(F.data.contains("delete"), IsAdmin())
async def delete_product(callback_query: types.CallbackQuery):
    link = callback_query.data.split()[2]
    product = Product.get_by_link(link)
    product.delete_product()
    await callback_query.message.answer("Product deleted")


def register_admin_callback_handlers(dp: Dispatcher):
    dp.include_router(router)
