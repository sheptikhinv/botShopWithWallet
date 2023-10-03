from aiogram.fsm.state import StatesGroup, State


class EditingProduct(StatesGroup):
    editing_title = State()
    editing_description = State()
    editing_price = State()
    editing_currency_code = State()
    editing_amount = State()
    editing_file_id = State()