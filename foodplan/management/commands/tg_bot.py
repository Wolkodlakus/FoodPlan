#from django.conf import settings
from django.core.management import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler, CommandHandler, Updater
from foodplan.models import Client
from telegram import LabeledPrice
from textwrap import dedent
import datetime
from dotenv import load_dotenv
import os
import foodplan.management.commands.keyboards as keyboards
import foodplan.management.commands.add_user_info as add_user_info
import foodplan.management.commands.states as states
import foodplan.management.commands.checks as checks
import foodplan.management.commands.funcs_db as funcs_db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            main()
        except Exception as exc:
            raise CommandError(exc)


def start(update, context):
    id_client = funcs_db.find_client(update.message.chat_id)
    if not id_client:
        logger.info(f'Не найден пользователь с chat_id {update.message.chat_id}')
        context.user_data['chat_id'] = update.message.chat_id
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
    context.user_data['client'] = Client.objects.get(id=id_client)
    logger.info(f'Пользователь с chat_id {update.message.chat_id} найден, это {context.user_data["client"].name}')
    update.message.reply_text(
        'Выберите действие:',
        reply_markup=keyboards.create_personal_area()
    )
    return states.States.PERSONAL_AREA


def handle_unknown(update, context):
    logger.info(f'Неизвестная команда')
    update.message.reply_text(
        text='Извините, но я вас не понял :(',
    )

def cancel(update: Update, context: CallbackContext):
    #user = update.message.from_user
    logger.info('Пользователь ввёл cancel')
    update.message.reply_text(
        'Пока!', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    WEEK, START_CALL_TIME, END_CALL_TIME = range(3)
    BUTTONS_IN_ROW = 4
    ROWS = 4

    #SK=settings.SECRET_KEY

    load_dotenv()
    token_tg = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token=token_tg)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
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
            CommandHandler('cancel', cancel),
            MessageHandler(Filters.text & ~Filters.command, handle_unknown),
        ],
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()