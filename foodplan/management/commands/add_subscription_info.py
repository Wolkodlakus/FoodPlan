import states
import keyboards
from textwrap import dedent


def input_subscription_name(update, context):
    update.message.reply_text(
        'Введите название подписки'
    )
    context.chat_data.clear()
    return states.States.CHOOSE_MENU_TYPE


def choose_menu_type(update, context):
    context.chat_data['sub_name'] = update.message.text
    update.message.reply_text(
        'Выберите тип меню:',
        reply_markup=keyboards.choose_menu_type()
    )
    return states.States.CHOOSE_PERSON_AMOUNT


def choose_person_amount(update, context):
    context.chat_data['menu_type'] = update.message.text
    update.message.reply_text(
        'Введите количество персон'
    )
    return states.States.CHOOSE_MEALS_AMOUNT


def choose_meals_amount(update, context):
    context.chat_data['person_amount'] = update.message.text
    update.message.reply_text(
        'Введите количество приемов пищи'
    )
    return states.States.CHOOSE_ALLERGIES


def choose_allergies(update, context):
    context.chat_data['meals_amount'] = update.message.text
    update.message.reply_text(
        'Выберите аллергию',
        reply_markup=keyboards.choose_allergies()
    )
    return states.States.CHOOSE_SUBSCRIPTIONS_TERM


def choose_subscriptions_term(update, context):
    context.chat_data['allergies'] = [update.message.text]
    update.message.reply_text(
        'Выберите срок подписки',
        reply_markup=keyboards.choose_subscriptions_term()
    )
    return states.States.OUTPUT_COST_AND_PARAMS


def output_cost_and_params(update, context):
    new_subscriptions = {
        'sub_name': context.chat_data['sub_name'],
        'menu_type': context.chat_data['menu_type'],
        'person_amount': context.chat_data['person_amount'],
        'meals_amount': context.chat_data['meals_amount'],
        'allergies': context.chat_data['allergies'],
        'sub_term': update.message.text,
        'cost': 1000
    }
    update.message.reply_text(
        dedent(f'''\
            Ваша подписка:
            Название: {new_subscriptions['sub_name']}
            Тип меню: {new_subscriptions['menu_type']}
            Количество персон: {new_subscriptions['person_amount']}
            Количество приемов пищи: {new_subscriptions['meals_amount']}
            Аллергии: {new_subscriptions['allergies']}
            Срок подписки: {new_subscriptions['sub_term']}
            
            Стоимость вашей подписки: 
            --//--
            Чтобы оплатить нажмите кнопку PAY'''),
        reply_markup=keyboards.pay()
    )
    print('We need to add current sub term in the db')
    return states.States.PAY
