from dotenv import load_dotenv

from foodplan.management.commands import keyboards
import states
import os
from telegram import LabeledPrice


def start_without_shipping_callback(update, context):
    """Sends an invoice without shipping-payment."""
    load_dotenv()
    provider_token = os.getenv('PROVIDER_TOKEN')
    bot_payload = os.getenv('BOT_PAYLOAD')

    client_id = update.message.chat_id

    title = "Оплата подписки"
    description = "Оплата подписки"
    payload = bot_payload
    currency = "RUB"
    price = 1000
    prices = [LabeledPrice("Test", int(price * 100))]

    context.bot.send_invoice(client_id, title, description, payload,
                             provider_token, currency, prices)
    return states.States.ADD_SUBSCRIPTION_TO_DB


def successful_payment_callback(update, context):
    client_id = update.message.chat_id
    update.message.reply_text(
        'Оплата прошла успешно',
        reply_markup=keyboards.create_personal_area()
    )
    print('Добавить подписку в БД')
    return states.States.PERSONAL_AREA


def precheckout_callback(update, context):
    """Answers the PreQecheckoutQuery"""
    load_dotenv()
    bot_payload = os.getenv('BOT_PAYLOAD')
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != bot_payload:
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)
