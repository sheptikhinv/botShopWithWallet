from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import User
from database.product import Product


def status_to_circle(status: str):
    if status == "active": return "🟢"
    if status == "inactive": return "🔴"
    return ""


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
    change_file_id_button = InlineKeyboardButton(text="Change photo",
                                                 callback_data=f"product change_file_id {product.link}")
    delete_product_button = InlineKeyboardButton(text="DELETE PRODUCT",
                                                 callback_data=f"product delete {product.link}")
    return InlineKeyboardMarkup(inline_keyboard=[
        [change_status_button],
        [change_title_button, change_description_button],
        [change_price_button, change_currency_button],
        [change_amount_button, change_file_id_button],
        [delete_product_button]])


def contact_button():
    contact = InlineKeyboardButton(text="Contact seller", url=f"tg://user?id={User.get_all_admins_ids()[0]}")
    return InlineKeyboardMarkup(inline_keyboard=[[contact]])


def contact_user_button(user_id: int):
    contact = InlineKeyboardButton(text="Contact user", url=f"tg://user?id={user_id}")
    return InlineKeyboardMarkup(inline_keyboard=[[contact]])


def empty_button():
    empty = InlineKeyboardButton(text="Pay your order in next message", callback_data="pay pay pay")
    return InlineKeyboardMarkup(inline_keyboard=[[empty]])


def pay_button(link: str):
    pay = InlineKeyboardButton(text="Pay", url=link)
    return InlineKeyboardMarkup(inline_keyboard=[[pay]])
