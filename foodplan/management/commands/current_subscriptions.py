from textwrap import dedent
import keyboards
import states
import foodplan.management.commands.checks as checks


def output_subscriptions(update, context):
    subscribes = checks.check_subscriptions(update.message.chat_id)
    if subscribes:
        update.message.reply_text(
            dedent(f'''\
                Вот ваши подписки:
                Чтобы посмотреть детальную информацию о подписке,
                нажмите соответствующую кнопку с ее названием.'''),
            reply_markup=keyboards.create_all_gamer_games_keyboard(
                subscribes
            )
        )
        return states.States.CURRENT_SUBSCRIPTIONS
    update.message.reply_text(
        'У вас пока нет подписок.',
        reply_markup=keyboards.create_personal_area()
    )
    return states.States.PERSONAL_AREA
