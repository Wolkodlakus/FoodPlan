from textwrap import dedent
import keyboards
import states
from foodplan.management.commands import checks


def output_subscriptions(update, context):
    print('Подписки надо брать из БД')
    if checks.checking_existence_subscriptions(update.message.chat_id):
        update.message.reply_text(
            dedent(f'''\
                Вот ваши подписки:
                Чтобы посмотреть детальную информацию о подписке,
                нажмите соответствующую кнопку с ее названием.'''),
            reply_markup=keyboards.create_all_gamer_games_keyboard(
                ['first', 'second', 'third']
            )
        )
        return states.States.CURRENT_SUBSCRIPTIONS
    update.message.reply_text(
        'У вас пока нет подписок.',
        reply_markup=keyboards.create_personal_area()
    )
    return states.States.PERSONAL_AREA
