import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name, description):
    """Создание продукта в Stripe"""

    return stripe.Product.create(name=name, description=description)


def create_stripe_price(product, amount):
    """Создание цены продукта в Stripe"""

    return stripe.Price.create(
        currency="rub",  # Валюта
        unit_amount=amount * 100,  # Цена продукта в рублях (в копейках)
        product_data={"name": product.name},  # Название продукта Stripe
    )


def create_stripe_session(price):
    """Создание сессии для оплаты в Stripe"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="transfer",  # Режим оплаты - перевод на счет
    )
    return session.get("id"), session.get("url")
