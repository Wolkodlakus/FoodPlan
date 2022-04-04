import foodplan.management.commands.states as states
import foodplan.management.commands.tg_bot as tg_bot
from foodplan.models import Client, DishViewSubscription, Subscription, Dish
from textwrap import dedent
import foodplan.management.commands.keyboards as keyboards


def get_dish(update, context):
    context.chat_data['subscription'] = update.message.text
    context.user_data['subscription'] = context.chat_data['subscription']
    print(context.user_data['subscription'])
    #пока поиск только по имени подписки. Нужно совместить с поиском по клиенту.
    id_dish = tg_bot.get_one_dish(update, context)
    if not id_dish:
        update.message.reply_text(
            'В этой подписке нет подходящих блюд',
            # reply_markup=keyboards.choose_subscriptions_term()
        )
        return states.States.PERSONAL_AREA
    dish = Dish.objects.get(id=id_dish)
    #Здесь нужна проверка на истечение срока
    update.send_photo(chat_id=update.message.chat_id, photo=dish.img)
    update.message.reply_text(
        dedent(f'''\
        Новое блюдо: {dish.name}
        Ингридиенты: {dish.ingredients}
        Рецепт: {dish.recipe}
        Совет: {dish.advice}
        Килокалорий:{dish.kkal}
        
        Чтобы выбрать другое блюдо нажмите кнопку Другое'''),
        reply_markup=keyboards.other()
    )

    return states.States.CURRENT_SUBSCRIPTIONS
