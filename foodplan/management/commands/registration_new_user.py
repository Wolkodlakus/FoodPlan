import os
from dotenv import load_dotenv
from textwrap import dedent

from telegram import LabeledPrice
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, PreCheckoutQueryHandler, Updater)
import keyboards
import add_user_info
import states
import checks


def start(update, context):
    if checks.check_new_user(update.message.chat_id):
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
                    add_user_info.add_current_phone
                ),
                MessageHandler(
                    Filters.regex('^Создать подписку'),
                    add_user_info.input_new_phone
                ),
            ],
        },
        fallbacks=[
            CommandHandler('start', start),
            MessageHandler(Filters.text & ~Filters.command, handle_unknown)
        ],
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


def main():

    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    run_bot(tg_token)


if __name__ == '__main__':
    main()
