import asyncio
import uuid

from WalletPay import AsyncWalletPayAPI
from WalletPay.types import OrderPreview
from aiogram.types import CallbackQuery

from bot.keyboards import contact_button, contact_user_button
from config import get_wallet_key
from database import Product, Order, User

api = AsyncWalletPayAPI(get_wallet_key())


async def create_new_order(product: Product, user_id: int) -> OrderPreview:
    external_id = str(uuid.uuid4())
    order = await api.create_order(
        amount=product.price,
        currency_code=product.currency_code,
        description=product.title,
        external_id=external_id,
        timeout_seconds=900,
        customer_telegram_user_id=str(user_id)
    )
    order_obj = Order(
        external_id=external_id,
        order_id=order.id,
        title=product.title,
        product_link=product.link,
        user_id=user_id,
        price=product.price,
        currency_code=product.currency_code,
        status=order.status
    )
    order_obj.add_to_database()
    return order


async def checking_and_finishing_order(order: OrderPreview, callback_query: CallbackQuery, product: Product):
    order_preview = order
    order_obj = Order.get_by_order_id(order_id=order.id)
    while order_preview.status == "ACTIVE":
        order_preview = await api.get_order_preview(order_id=order.id)
        if order_preview.status == "PAID":
            product.change_cell("amount", product.amount - 1)
            await callback_query.message.answer(text="Thanks for buying!\nPlease, contact seller for delivery options",
                                                reply_markup=contact_button())
            await callback_query.bot.send_message(chat_id=User.get_all_admins_ids()[0],
                                                  text=f"User {callback_query.from_user.first_name} just bought {product.title}.",
                                                  reply_markup=contact_user_button(callback_query.from_user.id))
        if order_preview.status == "EXPIRED":
            await callback_query.message.answer("Order expired.")
        if order_preview.status == "CANCELLED":
            await callback_query.message.answer("Order has been cancelled.")
        order_obj.change_cell("status", order_preview.status)
        await asyncio.sleep(30)
