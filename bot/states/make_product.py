from aiogram.fsm.state import StatesGroup, State


class MakeProduct(StatesGroup):
    setting_title = State()
    setting_description = State()
    setting_amount = State()
    setting_price = State()
    setting_currency = State()
    setting_file_id = State()
