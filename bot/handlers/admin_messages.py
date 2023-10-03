from aiogram import Router, Dispatcher, F, types
from aiogram.filters import or_f
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.filters import DoesAdminExist, IsAdmin
from bot.keyboards import list_of_products, admin_buttons
from bot.misc import create_new_product, format_product_for_admin
from bot.states import MakeProduct, EditingProduct
from database import User, Product

router = Router(name="admin_messages")


@router.message(F.text == "Кактус", ~DoesAdminExist())
async def set_admin(message: types.Message):
    user = User.get_from_database(message.from_user.id)
    user.set_role("admin")
    await message.answer("You've became administrator!")


@router.message(Command("create"), IsAdmin())
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(product_created_by=message.from_user.id)
    await message.answer(
        'Creating new product!!\nYou can send "/cancel" any moment to stop creating new product\nEnter product title:')
    await state.set_state(MakeProduct.setting_title)


@router.message(Command("cancel"), IsAdmin())
async def cancel_creation(message: types.Message, state: FSMContext):
    await message.answer("Okey, cancelling product creation")
    await state.clear()


@router.message(or_f(EditingProduct.editing_title, MakeProduct.setting_title), IsAdmin())
async def title_added(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditingProduct.editing_title:
        link = (await state.get_data())["product_link"]
        product = Product.get_by_link(link)
        product.change_cell("title", message.text)
        await state.clear()
        await message.answer("Title edited!")
    elif current_state == MakeProduct.setting_title:
        await state.update_data(product_title=message.text)
        await message.answer("Title added! Send product description:")
        await state.set_state(MakeProduct.setting_description)


@router.message(or_f(MakeProduct.setting_description, EditingProduct.editing_description), IsAdmin())
async def description_added(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditingProduct.editing_description:
        link = (await state.get_data())["product_link"]
        product = Product.get_by_link(link)
        product.change_cell("description", message.text)
        await state.clear()
        await message.answer("Description edited!")
    elif current_state == MakeProduct.setting_description:
        await state.update_data(product_description=message.text)
        await message.answer("Added description! Now enter amount (digits only):")
        await state.set_state(MakeProduct.setting_amount)


@router.message(or_f(MakeProduct.setting_amount, EditingProduct.editing_amount), F.text.isdigit(), IsAdmin())
async def amount_added(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditingProduct.editing_amount:
        link = (await state.get_data())["product_link"]
        product = Product.get_by_link(link)
        product.change_cell("amount", message.text)
        await state.clear()
        await message.answer("Amount edited!")
    elif current_state == MakeProduct.setting_amount:
        await state.update_data(product_amount=int(message.text))
        await message.answer("Amount added! Enter price (only digits) for 1 item:")
        await state.set_state(MakeProduct.setting_price)


@router.message(or_f(MakeProduct.setting_amount, EditingProduct.editing_amount), IsAdmin())
async def invalid_amount(message: types.Message):
    await message.answer("Sorry, you have to enter digits only!")


@router.message(or_f(MakeProduct.setting_price, EditingProduct.editing_price), F.text.isdigit(), IsAdmin())
async def price_added(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditingProduct.editing_price:
        link = (await state.get_data())["product_link"]
        product = Product.get_by_link(link)
        product.change_cell("price", message.text)
        await state.clear()
        await message.answer("Price edited!")
    elif current_state == MakeProduct.setting_price:
        await state.update_data(product_price=int(message.text))
        await message.answer("Added price. Send currency code for this product (for example USD or RUB):")
        await state.set_state(MakeProduct.setting_currency)


@router.message(or_f(MakeProduct.setting_price, EditingProduct.editing_price), IsAdmin())
async def invalid_price(message: types.Message):
    await message.answer("Sorry, you have to enter digits only!")


@router.message(or_f(MakeProduct.setting_currency, EditingProduct.editing_currency_code), F.text.len() == 3, IsAdmin())
async def currency_code_added(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditingProduct.editing_currency_code:
        link = (await state.get_data())["product_link"]
        product = Product.get_by_link(link)
        product.change_cell("currency_code", message.text)
        await state.clear()
        await message.answer("Currency edited!")
    elif current_state == MakeProduct.setting_currency:
        await state.update_data(product_currency_code=message.text.upper())
        await message.answer(
            'Great! Last step: if you want to add photo (max one) for product, send photo or send "/finish"')
        await state.set_state(MakeProduct.setting_file_id)


@router.message(or_f(MakeProduct.setting_currency, EditingProduct.editing_currency_code), IsAdmin())
async def invalid_currency(message: types.Message):
    await message.answer("Sorry, wrong currency code!")


@router.message(or_f(MakeProduct.setting_file_id, EditingProduct.editing_file_id), F.photo, IsAdmin())
async def file_id_added(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == EditingProduct.editing_file_id:
        link = (await state.get_data())["product_link"]
        product = Product.get_by_link(link)
        product.change_cell("file_id", message.photo[-1].file_id)
        await state.clear()
        await message.answer("Photo edited!")
    elif current_state == MakeProduct.setting_file_id:
        await state.update_data(product_file_id=message.photo[-1].file_id)
        await message.answer("Photo added, product is ready!")
        await preview_product(message, state, True)


@router.message(MakeProduct.setting_file_id, Command("finish"), IsAdmin())
async def preview_product(message: types.Message, state: FSMContext, with_photo: bool = False):
    user_data = await state.get_data()
    product_link = await create_new_product(user_data)
    if with_photo:
        await message.answer_photo(
            photo=user_data["product_file_id"],
            caption=f"{user_data['product_title']}\n\n"
                    f"{user_data['product_description']}\n\n"
                    f"Price: {user_data['product_price']} {user_data['product_currency_code']}\n"
                    f"Amount: {user_data['product_amount']}"
        )
    else:
        await message.answer(
            f"{user_data['product_title']}\n\n"
            f"{user_data['product_description']}\n\n"
            f"Price: {user_data['product_price']} {user_data['product_currency_code']}\n"
            f"Amount: {user_data['product_amount']}"
        )
    await message.answer(f"Product link: t.me/{(await message.bot.get_me()).username}?start={product_link}")
    await state.clear()


@router.message(Command("products"), IsAdmin())
async def get_products_by_admin(message: types.Message):
    await message.answer(
        text="Here all products:",
        reply_markup=list_of_products(is_admin=True)
    )


def register_admin_messages_handlers(dp: Dispatcher):
    dp.include_router(router)
