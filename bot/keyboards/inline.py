from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.misc import status_to_circle
from database.product import Product


def list_of_products(is_admin: bool):
    products = Product.get_all_products()
    buttons = []
    for product in products:
        if (is_admin and product.status == "inactive") or (product.status == "active"):
            text = ""
            if is_admin:
                text += status_to_circle(product.status)
            text += f"{product.title} - {product.price} {product.currency_code}"
            buttons.append([InlineKeyboardButton(
                text=text,
                callback_data=f"product get {product.link}"
            )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def user_buttons(product: Product):
    make_order_button = InlineKeyboardButton(text="Pay via Wallet", callback_data=f"product buy {product.link}")
    return InlineKeyboardMarkup(inline_keyboard=[[make_order_button]])


def admin_buttons(product: Product):
    change_status_button = InlineKeyboardButton(text="ACTIVE/INACTIVE",
                                                callback_data=f"product change_status {product.link}")
    change_title_button = InlineKeyboardButton(text="Change title",
                                               callback_data=f"product change_title {product.link}")
    change_description_button = InlineKeyboardButton(text="Change description",
                                                     callback_data=f"product change_description {product.link}")
    change_price_button = InlineKeyboardButton(text="Change price",
                                               callback_data=f"product change_price {product.link}")
    change_currency_button = InlineKeyboardButton(text="Change currency",
                                                  callback_data=f"product change_currency {product.link}")
    change_amount_button = InlineKeyboardButton(text="Change amount",
                                                callback_data=f"product change_amount {product.link}")
    change_file_id_button = InlineKeyboardButton(text = "Change photo",
                                                 callback_data=f"product change_file_id {product.link}")
    delete_product_button = InlineKeyboardButton(text="DELETE PRODUCT",
                                                 callback_data=f"product delete {product.link}")
    return InlineKeyboardMarkup(inline_keyboard=[
        [change_status_button],
        [change_title_button, change_description_button],
        [change_price_button, change_currency_button],
        [change_amount_button, change_file_id_button],
        [delete_product_button]])
