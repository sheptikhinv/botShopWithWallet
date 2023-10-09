import random
import string

from database.product import Product


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


async def create_new_product(user_data: dict):
    if not "product_file_id" in user_data:
        user_data["product_file_id"] = None
    product = Product(
        title=user_data["product_title"],
        description=user_data["product_description"],
        amount=user_data["product_amount"],
        price=user_data["product_price"],
        currency_code=user_data["product_currency_code"],
        created_by=user_data["product_created_by"],
        status="active",
        link=id_generator(),
        file_id=user_data["product_file_id"],
    )
    product.add_to_database()
    return product.link


async def format_product_for_admin(username: str, product: Product):
    text = (f"{product.title}\n\n"
            f"{product.description}\n\n"
            f"Price: {product.price} {product.currency_code}\n"
            f"Left: {product.amount}\n"
            f"Status: {product.status}\n\n"
            f"Product link: t.me/{username}?start={product.link}")

    return text


async def format_product(product: Product):
    text = (f"{product.title}\n\n"
            f"{product.description}\n\n"
            f"Price: {product.price} {product.currency_code}\n"
            f"Left: {product.amount}\n\n"
            f"Please make your selection carefully before ordering\n"
            f"Analog photography is a unique product and cannot be returned!\n"
            f"After payment, the photo is securely packaged and sent by mail within 7 days; other shipping options are discussed in person by correspondence.")

    return text
