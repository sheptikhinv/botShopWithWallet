from aiogram import Router, Dispatcher, F, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from bot.filters import DoesAdminExist, IsAdmin
from bot.states import MakeProduct
from database import User

router = Router(name="admin")


@router.message(F.text == "Кактус", ~DoesAdminExist())
async def set_admin(message: types.Message):
    user = User.get_from_database(message.from_user.id)
    user.set_role("admin")
    await message.answer("Вы стали администратором!")


@router.message(Command("create"), IsAdmin())
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        'Создаём новое объявление!\nВ любой момент вы можете отправить "/cancel", чтоб прекратить создание товара\nВведите название товара:')
    await state.set_state(MakeProduct.setting_title)


@router.message(MakeProduct.setting_title, IsAdmin())
async def title_added(message: types.Message, state: FSMContext):
    await state.update_data(product_title=message.text)
    await message.answer("Название создано! Отправьте описание товара:")
    await state.set_state(MakeProduct.setting_description)


@router.message(MakeProduct.setting_description, IsAdmin())
async def description_added(message: types.Message, state: FSMContext):
    await state.update_data(product_description=message.text)
    await message.answer("Добавлено описание! Теперь введите тираж (только цифры!):")
    await state.set_state(MakeProduct.setting_amount)


@router.message(MakeProduct.setting_amount, F.text.isdigit(), IsAdmin())
async def amount_added(message: types.Message, state: FSMContext):
    await state.update_data(product_amount=int(message.text))
    await message.answer("Тираж указан! Введите цену (опять только цифру!!) за 1 шт.:")
    await state.set_state(MakeProduct.setting_price)


@router.message(MakeProduct.setting_amount, IsAdmin())
async def invalid_amount(message: types.Message):
    await message.answer("Извините, отправьте только цифру для указания тиража!")


@router.message(MakeProduct.setting_price, F.text.isdigit(), IsAdmin())
async def price_added(message: types.Message, state: FSMContext):
    await state.update_data(product_price=int(message.text))
    await message.answer("Цена указана. Отправьте код валюты, используемой в данном товаре (например USD или RUB):")
    await state.set_state(MakeProduct.setting_currency)


@router.message(MakeProduct.setting_price, IsAdmin())
async def invalid_price(message: types.Message):
    await message.answer("Извините, отправьте только цифру для указания стоимости!")


@router.message(MakeProduct.setting_currency, F.text.len() == 3, IsAdmin())
async def currency_code_added(message: types.Message, state: FSMContext):
    await state.update_data(product_currency_code=message.text.upper())
    await message.answer(
        'Отлично! Последний шаг: если хотите добавить фотографию (максимум одну) к товару, отправьте это фото мне, либо напишите "/finish"')
    await state.set_state(MakeProduct.setting_file_id)


@router.message(MakeProduct.setting_currency, IsAdmin())
async def invalid_currency(message: types.Message):
    await message.answer("Извините, вы неправильно ввели код валюты!")


@router.message(MakeProduct.setting_file_id, F.photo, IsAdmin())
async def file_id_added(message: types.Message, state: FSMContext):
    await state.update_data(product_file_id=message.photo[-1].file_id)
    await message.answer("Фотография добавлена, товар готов!")
    await preview_product(message, state, True)


@router.message(MakeProduct.setting_file_id, Command("finish"), IsAdmin())
async def preview_product(message: types.Message, state: FSMContext, with_photo: bool = False):
    user_data = await state.get_data()
    if with_photo:
        await message.answer_photo(
            photo=user_data["product_file_id"],
            caption=f"{user_data['product_title']}\n\n"
                    f"{user_data['product_description']}\n\n"
                    f"Цена: {user_data['product_price']} {user_data['product_currency_code']}\n"
                    f"Тираж: {user_data['product_amount']}"
        )
    else:
        await message.answer(
            f"{user_data['product_title']}\n\n"
            f"{user_data['product_description']}\n\n"
            f"Цена: {user_data['product_price']} {user_data['product_currency_code']}\n"
            f"Тираж: {user_data['product_amount']}"
        )


## TODO: СДЕЛАТЬ СОЗДАНИЕ ССЫЛКИ НА ТОВАР

@router.message(Command("cancel"), IsAdmin())
async def cancel_creation(message: types.Message, state: FSMContext):
    await message.answer("Хорошо, отменяем создание товара!")
    await state.clear()


def register_admin_handlers(dp: Dispatcher):
    dp.include_router(router)
