from textwrap import dedent
import foodplan.management.commands.keyboards as keyboards
import foodplan.management.commands.states as states
import foodplan.management.commands.checks as checks


def output_subscriptions(update, context):
    subscriptions = checks.check_subscriptions(update.message.chat_id)
    print(subscriptions)
    print(type(subscriptions))
    if subscriptions:
        update.message.reply_text(
            dedent(f'''\
                Вот ваши подписки:
                Чтобы посмотреть детальную информацию о подписке,
                нажмите соответствующую кнопку с ее названием.'''),
            reply_markup=keyboards.create_all_subscriptions_keyboards(
                subscriptions
            )
        )
        return states.States.CURRENT_SUBSCRIPTIONS
    update.message.reply_text(
        'У вас пока нет подписок.',
        reply_markup=keyboards.create_personal_area()
    )
    return states.States.PERSONAL_AREA
