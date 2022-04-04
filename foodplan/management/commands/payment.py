import os

from dotenv import load_dotenv
from telegram import LabeledPrice

import foodplan.management.commands.funcs_db as funcs_db
import foodplan.management.commands.keyboards as keyboards
import foodplan.management.commands.states as states


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
    price = context.chat_data['new_subscriptions']['cost']
    prices = [LabeledPrice("Test", int(price * 100))]
    context.bot.send_invoice(client_id, title, description, payload,
                             provider_token, currency, prices)
    return states.States.PAY_BANK


def successful_payment_callback(update, context):
    client_id = update.message.chat_id
    update.message.reply_text(
        'Оплата прошла успешно',
        reply_markup=keyboards.create_personal_area()
    )
    print('Добавить подписку в БД')
    new_subscription = context.chat_data['new_subscription']
    funcs_db.add_subscription(
        funcs_db.find_client(update.message.chat_id),
        new_subscription['menu_type'],
        new_subscription['person_amount'],
        new_subscription['sub_term'],
        new_subscription['allergies']
    )
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
