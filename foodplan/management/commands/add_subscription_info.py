import foodplan.management.commands.states as states
import foodplan.management.commands.keyboards as keyboards
from textwrap import dedent
import foodplan.management.commands.funcs_db as funcs_db



def choose_menu_type(update, context):
    context.chat_data.clear()
    update.message.reply_text(
        'Выберите тип меню:',
        reply_markup=keyboards.choose_menu_type()
    )
    return states.States.CHOOSE_PERSON_AMOUNT


def get_menu_id(menu_name):
    all_menu = ('Классическое', 'Низкоуглеводное', 'Вегетарианское', 'Кето')
    return all_menu.index(menu_name) + 1


def choose_person_amount(update, context):
    context.chat_data['menu_type'] = get_menu_id(update.message.text)
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


def get_allergies_id(allergy_name):
    all_allergies = (
        'Нет',
        'Рыба и морепродукты',
        'Мясо',
        'Зерновые',
        'Продукты пчеловодства',
        'Орехи и бобовые',
        'Молочные продукты'
    )
    return [all_allergies.index(allergy_name) + 1]


def choose_subscriptions_term(update, context):
    context.chat_data['allergies'] = get_allergies_id(update.message.text)
    update.message.reply_text(
        'Выберите срок подписки',
        reply_markup=keyboards.choose_subscriptions_term()
    )
    return states.States.OUTPUT_COST_AND_PARAMS


def output_cost_and_params(update, context):
    new_subscriptions = {
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
    funcs_db.add_subscription(
        funcs_db.find_client(update.message.chat_id),
        new_subscriptions['menu_type'],
        new_subscriptions['person_amount'],
        new_subscriptions['sub_term'],
        new_subscriptions['allergies']
    )
    return states.States.PAY
