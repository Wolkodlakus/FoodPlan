from textwrap import dedent

import foodplan.management.commands.keyboards as keyboards
import foodplan.management.commands.states as states


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
    context.chat_data['person_amount'] = int(update.message.text)
    update.message.reply_text(
        'Введите количество приемов пищи'
    )
    return states.States.CHOOSE_ALLERGIES


def choose_allergies(update, context):
    context.chat_data['meals_amount'] = int(update.message.text)
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
    # context.chat_data['allergies'] = get_allergies_id(update.message.text)
    context.chat_data['allergies'] = update.message.text
    update.message.reply_text(
        'Выберите срок подписки',
        reply_markup=keyboards.choose_subscriptions_term()
    )

    return states.States.OUTPUT_COST_AND_PARAMS


def get_cost_subscriptions(update, context):
    if context.chat_data['menu_type'] == 'Классическое':
        cost = 100
    else:
        cost = 200
    cost = cost * (0.95 + 0.05 * context.chat_data['person_amount'])
    cost = cost * (0.95 + 0.05 * context.chat_data['meals_amount'])
    if context.chat_data['allergies'] != 'Нет':
        cost = cost * 1.5
    cost = cost * context.chat_data['sub_term']
    return cost


def output_cost_and_params(update, context):
    context.chat_data['sub_term'] = int(update.message.text)
    new_subscription = {
        'client_chat_id': update.message.chat_id,
        'menu_type': context.chat_data['menu_type'],
        'person_amount': context.chat_data['person_amount'],
        'meals_amount': context.chat_data['meals_amount'],
        'allergies': context.chat_data['allergies'],
        'sub_term': context.chat_data['sub_term'],
        'cost': get_cost_subscriptions(update, context)
    }
    context.chat_data['new_subscription'] = new_subscription
    update.message.reply_text(
        dedent(f'''\
            Ваша подписка:
            Тип меню: {new_subscription['menu_type']}
            Количество персон: {new_subscription['person_amount']}
            Количество приемов пищи: {new_subscription['meals_amount']}
            Аллергии: {new_subscription['allergies']}
            Срок подписки: {new_subscription['sub_term']}
            
            Стоимость вашей подписки: 
            {new_subscription['cost']}
            Чтобы оплатить нажмите кнопку PAY'''),
        reply_markup=keyboards.pay()
    )
    return states.States.PAY
