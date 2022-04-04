import foodplan.management.commands.states as states



def get_dish(update, context):
    context.chat_data['subscription'] = update.message.text
    #пока поиск только по имени подписки. Нужно совместить с поиском по клиенту.

    #Здесь нужна проверка на истечение срока
    update.message.reply_text(
        'Выберите срок подписки',
        #reply_markup=keyboards.choose_subscriptions_term()
    )

    return states.States.OUTPUT_COST_AND_PARAMS
