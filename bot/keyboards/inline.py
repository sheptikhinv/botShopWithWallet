from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.product import Product


def list_of_products(is_admin: bool):
    products = Product.get_all_products()
    buttons = []
    for product in products:
        if (is_admin and product.status == "inactive") or (product.status == "active"):
            buttons.append([InlineKeyboardButton(
                text=f"{product.title} - {product.price} {product.currency_code}",
                callback_data=f"product get {product.link}"
            )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def make_order(product: Product):
    make_order_button = InlineKeyboardButton(text="Купить", callback_data=f"product buy {product.link}")
    return InlineKeyboardMarkup(inline_keyboard=[[make_order_button]])


def change_status(product):
    change_status_button = InlineKeyboardButton(text="ACTIVE/INACTIVE",
                                                callback_data=f"product change_status {product.link}")
    return InlineKeyboardMarkup(inline_keyboard=[[change_status_button]])
