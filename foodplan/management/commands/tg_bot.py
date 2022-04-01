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
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            main()
        except Exception as exc:
            raise CommandError(exc)


def get_subscribes(update, context):

    subscriptions=funcs_db.get_client_subscriptions(context.user_data['client'].id)
    subscribes = []
    for item in subscriptions:
        subscribes.append(item.name)

    update.message.reply_text(
        dedent(f'''\
            Ваши подписки {' '.join(subscribes)} .
            Введите вашу фамилию:''')
    )

def get_dish(update, context):
    subscription = context.user_data['subscription']
    all_id_suitable_dishes = get_id_suitable_dishes(subscription)
    all_id_show_dishes = get_id_show_dishes(subscription)
    if not all_id_suitable_dishes:
        print('Нет подходящих блюд')
        return False
    if len(all_id_suitable_dishes) == len(all_id_show_dishes):
        print('Показаны все возможные блюда. Очищаем список показанных блюд')
        clear_show_dishes(subscription)
    all_id_no_show_dishes = []
    #случай с нолём
    for id_dish in all_id_suitable_dishes:
        if not (id_dish in all_id_show_dishes):
            all_id_no_show_dishes.append(id_dish)
    id_dish_show = random.choice(all_id_no_show_dishes)
    add_id_show_dish(subscription)
    return id_dish_show

def add_id_show_dish(subscription):
    pass

def clear_show_dishes(subscription):
    pass

def get_id_show_dishes(subscription):
    pass

def get_id_suitable_dishes(subscription):
    return True


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
                    get_subscribes
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