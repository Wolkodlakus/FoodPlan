import os
from dotenv import load_dotenv
from textwrap import dedent


from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, PreCheckoutQueryHandler, Updater)
import keyboards
import add_user_info
import states
import current_subscriptions
import add_subscription_info
import payment
import funcs_db


def start(update, context):
    if not funcs_db.find_client(update.message.chat_id):
        update.message.reply_text(
            dedent('''\
            Вы у нас впервые.
            Давайте зарегистрируемся.
            Чтобы вас идентифицировать, нужен номер телефона
            Если он совпадает с номером вашего ТГ аккаунта, нажмите "SEND"
            Если хотите ввести другой номер, нажмите "ADD"
            '''),
            reply_markup=keyboards.get_user_phone()
        )
        return states.States.ADD_USER_PHONE

    update.message.reply_text(
        'Выберите действие:',
        reply_markup=keyboards.create_personal_area()
    )
    return states.States.PERSONAL_AREA


def handle_unknown(update, context):
    update.message.reply_text(
        text='Извините, но я вас не понял :(',
    )


def run_bot(tg_token):
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],
        states={
            states.States.ADD_USER_PHONE: [
                MessageHandler(
                    Filters.contact,
                    add_user_info.add_current_phone
                ),
                MessageHandler(
                    Filters.regex('^ADD'),
                    add_user_info.input_new_phone
                ),
            ],
            states.States.INPUT_NEW_PHONE: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_user_info.add_new_phone
                ),

            ],
            states.States.INPUT_USER_SURNAME: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_user_info.input_surname
                ),
            ],
            states.States.INPUT_USER_NAME: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_user_info.input_name
                ),
            ],
            states.States.PERSONAL_AREA: [
                MessageHandler(
                    Filters.regex('^Мои подписки'),
                    current_subscriptions.output_subscriptions
                ),
                MessageHandler(
                    Filters.regex('^Создать подписку'),
                    add_subscription_info.choose_menu_type
                ),
            ],
            states.States.CHOOSE_PERSON_AMOUNT: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_subscription_info.choose_person_amount
                ),
            ],
            states.States.CHOOSE_MEALS_AMOUNT: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_subscription_info.choose_meals_amount
                ),
            ],
            states.States.CHOOSE_ALLERGIES: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_subscription_info.choose_allergies
                ),
            ],
            states.States.CHOOSE_SUBSCRIPTIONS_TERM: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_subscription_info.choose_subscriptions_term
                ),
            ],
            states.States.OUTPUT_COST_AND_PARAMS: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    add_subscription_info.output_cost_and_params
                ),
            ],
            states.States.PAY: [
                MessageHandler(
                    Filters.regex('^PAY'),
                    payment.start_without_shipping_callback
                ),
            ],
            states.States.ADD_SUBSCRIPTION_TO_DB: [
                MessageHandler(
                    Filters.successful_payment,
                    payment.successful_payment_callback
                ),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(Filters.text & ~Filters.command, handle_unknown)
        ],
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(PreCheckoutQueryHandler(payment.precheckout_callback))

    updater.start_polling()
    updater.idle()


def main():

    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')

    run_bot(tg_token)


if __name__ == '__main__':
    main()
